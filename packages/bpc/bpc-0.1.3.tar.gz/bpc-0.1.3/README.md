# <div align="center"> BURMESE PHONEMIZER AND CLEANER(BPC) </div>

<div align="center">

[![Python package](https://github.com/1chimaruGin/Burmese_Phomizer_and_Cleaner/actions/workflows/python-package.yml/badge.svg)](https://github.com/1chimaruGin/Burmese_Phomizer_and_Cleaner/actions/workflows/python-package.yml)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/1chimaruGin/Burmese_Phomizer_and_Cleaner.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/1chimaruGin/Burmese_Phomizer_and_Cleaner/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/1chimaruGin/Burmese_Phomizer_and_Cleaner.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/1chimaruGin/Burmese_Phomizer_and_Cleaner/context:python)

<p>Burmese Language data prepartion for speech related tasks.</p>
<p>
</p>
</div>

## Installation

```bash
$ pip install bpc
```
or
```bash
$ pip install git+git://github.com:1chimaruGin/Burmese_Phomizer_and_Cleaner.git
```

## Usage

**For text Cleaning**
```python
from bpc import Cleaner

cc = Cleaner()
cc.clean_text("မင်္ဂလာပါ? မင်္ဂလာပါ။ ၀န်းရံ ဝ၁၂၃၄ 5B")

# output: မင်္ဂလာပါ မင်္ဂလာပါ။ ဝန်းရံ ၀၁၂၃၄ ၅ဘီ
```

**For phonemization**

```python
from bpc import BurmesePhoneme

bp = BurmesePhonemizer()
bp.text_to_phone("မင်္ဂလာပါ")

# output: ['m', 'ŋ', 'ɡ', 'l', 't', 's', 'p', 'ˈe']
```

**For data preparation**

```python
from bpc.dataset import PrepareDataset

dataset = PrepareDataset()
dataset.prepare_data(path='path/to/dataset', method='kfold', save=True)
```
## References

* https://github.com/espnet/espnet
* https://github.com/bootphon/phonemizer

## Citations

```
@inproceedings{watanabe2018espnet,
  author={Shinji Watanabe and Takaaki Hori and Shigeki Karita and Tomoki Hayashi and Jiro Nishitoba and Yuya Unno and Nelson {Enrique Yalta Soplin} and Jahn Heymann and Matthew Wiesner and Nanxin Chen and Adithya Renduchintala and Tsubasa Ochiai},
  title={{ESPnet}: End-to-End Speech Processing Toolkit},
  year={2018},
  booktitle={Proceedings of Interspeech},
  pages={2207--2211},
  doi={10.21437/Interspeech.2018-1456},
  url={http://dx.doi.org/10.21437/Interspeech.2018-1456
}

@article{Bernard2021,
  doi = {10.21105/joss.03958},
  url = {https://doi.org/10.21105/joss.03958},
  year = {2021},
  publisher = {The Open Journal},
  volume = {6},
  number = {68},
  pages = {3958},
  author = {Mathieu Bernard and Hadrien Titeux},
  title = {Phonemizer: Text to Phones Transcription for Multiple Languages in Python},
  journal = {Journal of Open Source Software}
}
```
