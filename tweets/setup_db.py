
import pandas as pd
from .models import *


def add_users():
    file = 'data/user_ids.csv'
    accs = pd.read_csv(file, index_col=0)
    for i, row in accs.iterrows():
        TwitterAcc.objects.create(username=i, user_id=row['id'])


def add_nfts():
    file = 'data/nftki.csv'
    nfts = pd.read_csv(file, index_col=0)
    for i, row in nfts.iterrows():
        NFT.objects.create(name=row['NFT'])


def setup_categories():
    for cat in ['Historical', 'Collectibles', 'Artwork', 'Gaming', 'Domain names']:
        Category.objects.create(name=cat)
    print('finito categories')


def nft_tags():
    nfts = NFT.objects.all()
    for nft in nfts:
        split = nft.name.split()
        if len(split) > 2:
            continue
        else:
            tag = Tag.objects.create(text="".join([s[0].lower() for s in split]))
            nft.tags.add(tag)
            nft.save()

    print('finito tags')