# 3Rs:Data Augmentation Techniques Using Document Contexts For Low-Resource Chinese Named Entity Recognition

This is the companion repository for our paper also available on ArXiv titled " 3Rs:Data Augmentation Techniques Using Document Contexts For Low-Resource Chinese Named Entity Recognition". This paper has been accepted at the IEEE International Joint Conference on Neural Networks (IJCNN) 2022.

## Approach
### Random Concatenating
![image](https://user-images.githubusercontent.com/57606213/169530368-498c3727-37f0-4cb6-ba5e-6a6f008b30a5.png)

### Random Erasing
![image](https://user-images.githubusercontent.com/57606213/169530496-0e39cbc5-35ef-4545-a9f4-c974b1e7b7b8.png)

### Random Swapping
![image](https://user-images.githubusercontent.com/57606213/169530553-342ee182-6e58-44cd-af7f-135235e94e55.png)

## Data
### Data Format
The data format used in our experiment is following the format of CLUENER（https://github.com/CLUEbenchmark/CLUENER）:

Example:

*{'text': '譬如《水淹七军》这出戏，关公和庞德厮杀了许多回合，竟不能取胜，无奈退回大营，唱起了：“阵前胜不过庞德将，且把春秋仔细观！”新华社开罗１月１０日电（侯嘉、王亚东）埃及外长穆萨１０日说，他和挪威外交大臣沃勒贝克都认为，中东和平进程继续向前推进的希望“十分渺茫”。', 'label': {'LOC': {'大营': [[35, 36]], '开罗': [[64, 65]], '埃及': [[80, 81]], '挪威': [[93, 94]], '中东': [[107, 108]]}, 'PER': {'关公': [[12, 13]], '庞德': [[15, 16], [48, 49]], '侯嘉': [[73, 74]], '王亚东': [[76, 78]], '穆萨': [[84, 85]], '沃勒贝克': [[99, 102]]}}}*

Ontonotes4.0 dataset: The official Ontonotes datasets can be obtained from: https://www.ldc.upenn.edu/language-resources

MSRA dataset:Our dataset is based on: https://github.com/lemonhu/NER-BERT-pytorch/tree/master/data/msra

## Code

The code is presented as follows:

randomcondatenating.py: implementation of random concatenating.

randomerasing.py:implementation of random erasing.

randomswapping.py:implementation of random swapping.

adversial_sample.ipynb:implementation of two-level adversarial attack generating.

Codes of BERT-Tagger\BERT-MRC\BERT-CRF\EDA\LDA can all be found in their original papers.

## Reference
If you are reusing this work, please cite:

@InProceedings{alexsivan,
  Title                    = {3Rs:Data Augmentation Techniques Using Document Contexts For Low-Resource Chinese Named Entity Recognition},
  Author                   = {Zheyu Ying ,Jinglei Zhang ,Rui Xie ,Guochang Wen ,Feng Xiao, Xueyang Liu ,Shikun Zhang},
  booktitle                = {IEEE International Joint Conference on Neural Networks},
  Year                     = {2022}
}
