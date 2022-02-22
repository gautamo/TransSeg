import os
import json
import pytorch_lightning as pl
import torch
from functools import partial
import random
import copy
import numpy as np

from monai.transforms import (
    AsDiscrete,
    AddChanneld,
    Compose,
    CropForegroundd,
    LoadImaged,
    Orientationd,
    RandFlipd,
    RandCropByPosNegLabeld,
    RandSpatialCropSamplesd,
    RandShiftIntensityd,
    ScaleIntensityRanged,
    Spacingd,
    RandRotate90d,
    ToTensord,
    Resized,
    RandZoomd,
    RandSpatialCropd,
    SpatialPadd,
    MapTransform,
    Randomizable,
)
from monai.data import (
    DataLoader,
    CacheDataset,
    load_decathlon_datalist,
    decollate_batch,
)


class Windowingd(MapTransform):
    """
    Performs windowing to the data, each window contains N slices.
    """

    def __init__(
        self,
        size=5,
        keys=["image", "label"],
        allow_missing_keys=False,
    ) -> None:
        """
        Args:
            size: number of slices within each window.
        """
        super().__init__(keys, allow_missing_keys)
        assert size % 2 == 1
        self.size = size
        self.pad = size // 2

    def __call__(self, data):

        padded_data = {}
        for key in self.keys:
            assert len(data[key].shape) == 4
            padded_data[key] = np.zeros(
                (
                    data[key].shape[0],
                    data[key].shape[1],
                    data[key].shape[2],
                    data[key].shape[3] + self.pad * 2,
                )
            ).astype(data[key].dtype)
            padded_data[key][..., self.pad : -self.pad] = data[key]
            for i in range(self.pad):
                padded_data[key][..., i] = data[key][..., 0]
            for i in range(self.pad):
                padded_data[key][..., -i - 1] = data[key][..., -1]

        ret = []
        n_slices = data[self.keys[0]].shape[-1]
        for i in range(n_slices):
            window_new = copy.deepcopy(data)
            for key in self.keys:
                window_new[key] = padded_data[key][..., i : i + self.size]
            ret.append(window_new)

        return ret


class NIIDataLoader(pl.LightningDataModule):
    def __init__(
        self,
        data_dir: str = "data/bcv30/bcv18-12-5slices/",
        split_json="dataset_5slices.json",
        img_size: tuple = (512, 512, 5),
        in_channels: int = 1,
        unit_range: tuple = (-175, 250),
        train_batch_size: int = 2,
        eval_batch_size: int = 2,
    ):
        super().__init__()
        self.data_dir = data_dir
        self.split_json = split_json
        self.img_size = img_size
        self.in_channels = in_channels
        self.unit_range = unit_range
        self.train_batch_size = train_batch_size
        self.eval_batch_size = eval_batch_size

        (
            self.train_transforms,
            self.val_transforms,
            self.test_transforms,
        ) = self.create_transforms()

    def create_transforms(self):
        train_transforms = Compose(
            [
                LoadImaged(keys=["image", "label"]),
                AddChanneld(keys=["image", "label"])
                if self.in_channels == 1
                else AddChanneld(keys=["label"]),
                Resized(keys=["image", "label"], spatial_size=self.img_size, mode=['area', 'nearest']),
                # Windowingd(keys=["image", "label"], size=5),
                RandZoomd(
                    keys=["image", "label"],
                    min_zoom=0.5,
                    max_zoom=2.0,
                    prob=1,
                    mode=["area", "nearest"],
                    keep_size=False,
                ),
                RandSpatialCropd(
                    keys=["image", "label"], roi_size=self.img_size, random_size=False
                ),
                # Spacingd(
                #     keys=["image", "label"],
                #     pixdim=(1.5, 1.5, 2.0),
                #     mode=("bilinear", "nearest"),
                # ),
                # Orientationd(keys=["image", "label"], axcodes="RAS"),
                ScaleIntensityRanged(
                    keys=["image"],
                    a_min=self.unit_range[0],
                    a_max=self.unit_range[1],
                    b_min=0.0,
                    b_max=1.0,
                    clip=True,
                ),
                # CropForegroundd(keys=["image", "label"], source_key="image"),
                # RandSpatialCropSamplesd(
                #     keys=["image", "label"],
                #     roi_size=(96, 96, 96),
                #     num_samples=4,
                #     random_size=False),
                # RandCropByPosNegLabeld(
                #     keys=["image", "label"],
                #     label_key="label",
                #     spatial_size=(96, 96, 96),
                #     pos=1,
                #     neg=1,
                #     num_samples=4,
                #     image_key="image",
                #     image_threshold=0,
                # ),
                RandFlipd(
                    keys=["image", "label"],
                    spatial_axis=[0],
                    prob=0.10,
                ),
                RandFlipd(
                    keys=["image", "label"],
                    spatial_axis=[1],
                    prob=0.10,
                ),
                RandFlipd(
                    keys=["image", "label"],
                    spatial_axis=[2],
                    prob=0.10,
                ),
                RandRotate90d(
                    keys=["image", "label"],
                    prob=0.10,
                    max_k=3,
                ),
                RandShiftIntensityd(
                    keys=["image"],
                    offsets=0.10,
                    prob=0.50,
                ),
                SpatialPadd(keys=["image", "label"], spatial_size=self.img_size),
                ToTensord(keys=["image", "label"]),
            ]
        )
        val_transforms = Compose(
            [
                LoadImaged(keys=["image", "label"]),
                AddChanneld(keys=["image", "label"])
                if self.in_channels == 1
                else AddChanneld(keys=["label"]),
                Resized(keys=["image", "label"], spatial_size=self.img_size, mode=['area', 'nearest']),
                # Windowingd(keys=["image", "label"], size=5),
                # Spacingd(
                #     keys=["image", "label"],
                #     pixdim=(1.5, 1.5, 2.0),
                #     mode=("bilinear", "nearest"),
                # ),
                # Orientationd(keys=["image", "label"], axcodes="RAS"),
                ScaleIntensityRanged(
                    keys=["image"],
                    a_min=self.unit_range[0],
                    a_max=self.unit_range[1],
                    b_min=0.0,
                    b_max=1.0,
                    clip=True,
                ),
                # CropForegroundd(keys=["image", "label"], source_key="image"),
                ToTensord(keys=["image", "label"]),
            ]
        )
        test_transforms = Compose(
            [
                LoadImaged(keys=["image"]),
                AddChanneld(keys=["image"]),
                # Windowingd(keys=["image", "label"], size=5),
                ScaleIntensityRanged(
                    keys=["image"],
                    a_min=self.unit_range[0],
                    a_max=self.unit_range[1],
                    b_min=0.0,
                    b_max=1.0,
                    clip=True,
                ),
                ToTensord(keys=["image"]),
            ]
            if self.in_channels == 1
            else [
                LoadImaged(keys=["image"]),
                # Windowingd(keys=["image"], size=5),
                ScaleIntensityRanged(
                    keys=["image"],
                    a_min=self.unit_range[0],
                    a_max=self.unit_range[1],
                    b_min=0.0,
                    b_max=1.0,
                    clip=True,
                ),
                ToTensord(keys=["image"]),
            ]
        )
        return train_transforms, val_transforms, test_transforms

    def setup(self, stage=None):
        data_config_file = f"{self.data_dir}/{self.split_json}"
        data_config = json.load(open(data_config_file))
        print(f"Loading data config from {data_config_file}...")

        train_files = load_decathlon_datalist(data_config_file, data_list_key="training")
        val_files = load_decathlon_datalist(data_config_file, data_list_key="validation")
        test_files = load_decathlon_datalist(data_config_file, data_list_key="local_test")

        self.train_ds = CacheDataset(
            data=train_files,
            transform=self.train_transforms,
            num_workers=6,
            cache_num=64,
        )
        self.val_ds = CacheDataset(
            data=val_files, 
            transform=self.val_transforms, 
            num_workers=3, 
            cache_num=64
        )
        self.test_ds = CacheDataset(
            data=test_files,
            transform=self.val_transforms, # set to test_transforms when submitting leaderboard
            num_workers=3,
            cache_num=64
        )
        print(
            f"# Train: {len(self.train_ds)}, # Val: {len(self.val_ds)}, # Test: {len(self.test_ds)}..."
        )

    def train_dataloader(self):
        return DataLoader(
            self.train_ds,
            batch_size=self.train_batch_size,
            shuffle=True,
            num_workers=6,
            pin_memory=True,
        )

    def val_dataloader(self):
        return DataLoader(
            self.val_ds,
            batch_size=self.eval_batch_size,
            shuffle=False,
            num_workers=3,
            pin_memory=True,
        )

    def test_dataloader(self):
        return DataLoader(
            self.test_ds,
            batch_size=self.eval_batch_size,
            shuffle=False,
            num_workers=3,
            pin_memory=True,
        )


if __name__ == "__main__":
    dm = NIIDataLoader(data_dir="jsons/", split_json="dataset.json")
    dm.setup()
    # print(dm.train_ds[0]['image'].shape, dm.train_ds[0]['label'].shape)
    print(dm.val_ds[0]["image"].shape, dm.val_ds[0]["label"].shape)
    input("To be continued...")
    for batch in dm.train_dataloader():
        print([key for key in batch])
        print(
            [
                (key, batch[key].shape)
                for key in batch
                if isinstance(batch[key], torch.Tensor)
            ]
        )
        break
