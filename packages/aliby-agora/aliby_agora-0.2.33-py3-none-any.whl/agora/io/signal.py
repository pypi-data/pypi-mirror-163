from copy import copy
from pathlib import PosixPath
from typing import Union

import h5py
import numpy as np
import pandas as pd
from utils_find_1st import cmp_larger, find_1st

from agora.io.bridge import BridgeH5


class Signal(BridgeH5):
    """
    Class that fetches data from the hdf5 storage for post-processing
    """

    def __init__(self, file: Union[str, PosixPath]):
        super().__init__(file, flag=None)

        self.names = ["experiment", "position", "trap"]

    def __getitem__(self, dsets):

        if isinstance(dsets, str) and dsets.endswith("imBackground"):
            df = self.get_raw(dsets)

        elif isinstance(dsets, str):
            df = self.apply_prepost(dsets)

        elif isinstance(dsets, list):
            is_bgd = [dset.endswith("imBackground") for dset in dsets]
            assert sum(is_bgd) == 0 or sum(is_bgd) == len(
                dsets
            ), "Trap data and cell data can't be mixed"
            return [
                self.add_name(self.apply_prepost(dset), dset) for dset in dsets
            ]

        # return self.cols_in_mins(self.add_name(df, dsets))
        return self.add_name(df, dsets)

    @staticmethod
    def add_name(df, name):
        df.name = name
        return df

    def cols_in_mins(self, df: pd.DataFrame):
        # Convert numerical columns in a dataframe to minutes
        try:
            df.columns = (df.columns * self.tinterval // 60).astype(int)
        except Exception as e:
            print(
                """
                Warning:Can't convert columns to minutes. Signal {}.{}""".format(
                    df.name, e
                )
            )
        return df

    @property
    def ntimepoints(self):
        with h5py.File(self.filename, "r") as f:
            return f["extraction/general/None/area/timepoint"][-1] + 1

    @property
    def tinterval(self):
        with h5py.File(self.filename, "r") as f:
            return f.attrs["time_settings/timeinterval"]

    @staticmethod
    def get_retained(df, cutoff):
        return df.loc[df.notna().sum(axis=1) > df.shape[1] * cutoff]

    def retained(self, signal, cutoff=0.8):

        df = self[signal]
        if isinstance(df, pd.DataFrame):
            return self.get_retained(df, cutoff)

        elif isinstance(df, list):
            return [self.get_retained(d) for d in df]

    def apply_prepost(self, dataset: str, skip_pick: bool = None):
        """
        Apply modifier operations (picker, merger) to a given dataframe.
        """
        merges = self.get_merges()
        df = self.get_raw(dataset)
        merged = copy(df)
        if merges.any():
            # Split in two dfs, one with rows relevant for merging and one
            # without them
            valid_merges = merges[
                (
                    merges[:, :, :, None]
                    == np.array(list(df.index)).T[:, None, :]
                )
                .all(axis=(1, 2))
                .any(axis=1)
            ]  # Casting allows fast multiindexing

            merged = self.apply_merge(
                df.loc[map(tuple, valid_merges.reshape(-1, 2))],
                valid_merges,
            )

            nonmergeable_ids = df.index.difference(valid_merges.reshape(-1, 2))

            merged = pd.concat(
                (merged, df.loc[nonmergeable_ids]), names=df.index.names
            )

        with h5py.File(self.filename, "r") as f:
            if "modifiers/picks" in f and not skip_pick:
                picks = self.get_picks(names=merged.index.names)
                # missing_cells = [i for i in picks if tuple(i) not in
                # set(merged.index)]

                if picks:
                    return merged.loc[
                        set(picks).intersection(
                            [tuple(x) for x in merged.index]
                        )
                    ]
                    return merged.loc[picks]
                else:
                    if isinstance(merged.index, pd.MultiIndex):
                        empty_lvls = [[] for i in merged.index.names]
                        index = pd.MultiIndex(
                            levels=empty_lvls,
                            codes=empty_lvls,
                            names=merged.index.names,
                        )
                    else:
                        index = pd.Index([], name=merged.index.name)
                    merged = pd.DataFrame([], index=index)
        return merged

    @property
    def datasets(self):
        if not hasattr(self, "_siglist"):
            self._siglist = []

            with h5py.File(self.filename, "r") as f:
                f.visititems(self.get_siglist)

        for sig in self.siglist:
            print(sig)

    @property
    def p_siglist(self):
        """Print signal list"""
        self.datasets

    @property
    def siglist(self):
        """Return list of signals"""
        try:
            if not hasattr(self, "_siglist"):
                self._siglist = []
                with h5py.File(self.filename, "r") as f:
                    f.visititems(self.get_siglist)
        except Exception as e:
            print("Error visiting h5: {}".format(e))
            self._siglist = []

        return self._siglist

    def get_merged(self, dataset):
        return self.apply_prepost(dataset, skip_pick=True)

    @property
    def merges(self):
        with h5py.File(self.filename, "r") as f:
            dsets = f.visititems(self._if_merges)
        return dsets

    @property
    def n_merges(self):
        print("{} merge events".format(len(self.merges)))

    @property
    def picks(self):
        with h5py.File(self.filename, "r") as f:
            dsets = f.visititems(self._if_picks)
        return dsets

    def apply_merge(self, df, changes):
        if len(changes):

            for target, source in changes:
                df.loc[tuple(target)] = self.join_tracks_pair(
                    df.loc[tuple(target)], df.loc[tuple(source)]
                )
                df.drop(tuple(source), inplace=True)

        return df

    def get_raw(self, dataset, in_minutes=True):
        try:
            if isinstance(dataset, str):
                with h5py.File(self.filename, "r") as f:
                    df = self.dset_to_df(f, dataset)
                    if in_minutes:
                        df = self.cols_in_mins(df)
                    return df
            elif isinstance(dataset, list):
                return [self.get_raw(dset) for dset in dataset]
        except Exception as e:
            print(f"Could not fetch dataset {dataset}")
            print(e)

    def get_merges(self):
        # fetch merge events going up to the first level
        with h5py.File(self.filename, "r") as f:
            merges = f.get("modifiers/merges", np.array([]))
            if not isinstance(merges, np.ndarray):
                merges = merges[()]

        return merges

    # def get_picks(self, levels):
    def get_picks(self, names, path="modifiers/picks/"):
        with h5py.File(self.filename, "r") as f:
            if path in f:
                return list(zip(*[f[path + name] for name in names]))
                # return f["modifiers/picks"]
            else:
                return None

    def dset_to_df(self, f, dataset):
        dset = f[dataset]
        names = copy(self.names)
        if not dataset.endswith("imBackground"):
            names.append("cell_label")
        lbls = {lbl: dset[lbl][()] for lbl in names if lbl in dset.keys()}
        index = pd.MultiIndex.from_arrays(
            list(lbls.values()), names=names[-len(lbls) :]
        )

        columns = (
            dset["timepoint"][()]
            if "timepoint" in dset
            else dset.attrs["columns"]
        )

        df = pd.DataFrame(dset[("values")][()], index=index, columns=columns)

        return df

    @staticmethod
    def dataset_to_df(f: h5py.File, path: str):

        all_indices = ["experiment", "position", "trap", "cell_label"]
        indices = {
            k: f[path][k][()] for k in all_indices if k in f[path].keys()
        }
        return pd.DataFrame(
            f[path + "/values"][()],
            index=pd.MultiIndex.from_arrays(
                list(indices.values()), names=indices.keys()
            ),
            columns=f[path + "/timepoint"][()],
        )

    def get_siglist(self, name: str, node):
        fullname = node.name
        if isinstance(node, h5py.Group) and np.all(
            [isinstance(x, h5py.Dataset) for x in node.values()]
        ):
            self._if_ext_or_post(fullname, self._siglist)

    @staticmethod
    def _if_ext_or_post(name: str, siglist: list):
        if name.startswith("/extraction") or name.startswith(
            "/postprocessing"
        ):
            siglist.append(name)

    @staticmethod
    def _if_merges(name: str, obj):
        if isinstance(obj, h5py.Dataset) and name.startswith(
            "modifiers/merges"
        ):
            return obj[()]

    @staticmethod
    def _if_picks(name: str, obj):
        if isinstance(obj, h5py.Group) and name.endswith("picks"):
            return obj[()]

    @staticmethod
    def join_tracks_pair(target: pd.Series, source: pd.Series):
        """
        Join two tracks
        """
        tgt_copy = copy(target)
        end = find_1st(target.values[::-1], 0, cmp_larger)
        tgt_copy.iloc[-end:] = source.iloc[-end:].values
        return tgt_copy
