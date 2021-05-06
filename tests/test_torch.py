from pathlib import Path

import pytorch_lightning as pl
import torch
import torch.nn.functional as F
import torchvision.models as models
from torch.utils.data import DataLoader
from torchvision.datasets import FashionMNIST
from torchvision.transforms import Compose, ToTensor


class MyModel(pl.LightningModule):

    def __init__(self):
        super().__init__()
        self.net = models.mobilenet_v2()

    def forward(self, x):
        return self.net(x)

    def training_step(self, batch, batch_idx):
        x, y = batch
        x = x.view(x.size(0), -1)
        y_hat = self(x)
        loss = F.mse_loss(y_hat, y)
        return loss

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=1e-3)
        return optimizer


root_dir = Path('D:/tmp')


def main():
    input_size = 32
    dataset = FashionMNIST(
        root_dir,
        download=True,
        transform=Compose([
            # RandomCrop(input_size),
            ToTensor(),
        ])
    )

    loader = DataLoader(
        dataset,
        batch_size=32,
        # num_workers=8,
    )

    model = MyModel()
    trainer = pl.Trainer(
        default_root_dir=root_dir
    )
    trainer.fit(model, loader)


if __name__ == '__main__':
    main()
