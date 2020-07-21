---
layout: archive
title: "Publications"
permalink: /publications/
author_profile: true
---

{% if author.googlescholar %}
  You can also find my articles on <u><a href="{{author.googlescholar}}">my Google Scholar profile</a>.</u>
{% endif %}

{% include base_path %}

{% for post in site.publications reversed %}
  {% include archive-single.html %}
{% endfor %}

@article{shen2017combinatorial,
  title={Combinatorial CRISPR--Cas9 screens for de novo mapping of genetic interactions},
  author={Shen, John Paul and Zhao, Dongxin and Sasik, Roman and Luebeck, Jens and Birmingham, Amanda and Bojorquez-Gomez, Ana and Licon, Katherine and Klepper, Kristin and Pekin, Daniel and Beckett, Alex N and others},
  journal={Nature methods},
  volume={14},
  number={6},
  pages={573--576},
  year={2017},
  publisher={Nature Publishing Group}
}

@article{zhao2018combinatorial,
  title={Combinatorial CRISPR-Cas9 Metabolic Screens Reveal Critical Redox Control Points Dependent on the KEAP1-NRF2 Regulatory Axis},
  author={Zhao, Dongxin and Badur, Mehmet G and Luebeck, Jens and Maga{\~n}a, Jose H and Birmingham, Amanda and Sasik, Roman and Ahn, Christopher S and Ideker, Trey and Metallo, Christian M and Mali, Prashant},
  journal={Molecular cell},
  volume={69},
  number={4},
  pages={699--708},
  year={2018},
  publisher={Elsevier}
}

@article{gray2018quantitative,
  title={Quantitative missense variant effect prediction using large-scale mutagenesis data},
  author={Gray, Vanessa E and Hause, Ronald J and Luebeck, Jens and Shendure, Jay and Fowler, Douglas M},
  journal={Cell systems},
  volume={6},
  number={1},
  pages={116--124},
  year={2018},
  publisher={Elsevier}
}

@article{nguyen2018vifi,
  title={ViFi: accurate detection of viral integration and mRNA fusion reveals indiscriminate and unregulated transcription in proximal genomic regions in cervical cancer},
  author={Nguyen, Nam-phuong D and Deshpande, Viraj and Luebeck, Jens and Mischel, Paul S and Bafna, Vineet},
  journal={Nucleic acids research},
  volume={46},
  number={7},
  pages={3309--3325},
  year={2018},
  publisher={Oxford University Press}
}

@article{deshpande2019exploring,
  title={Exploring the landscape of focal amplifications in cancer using AmpliconArchitect},
  author={Deshpande, Viraj and Luebeck, Jens and Nguyen, Nam-Phuong D and Bakhtiari, Mehrdad and Turner, Kristen M and Schwab, Richard and Carter, Hannah and Mischel, Paul S and Bafna, Vineet},
  journal={Nature communications},
  volume={10},
  number={1},
  pages={1--14},
  year={2019},
  publisher={Nature Publishing Group}
}

@article{rajkumar2019ecseg,
  title={EcSeg: Semantic Segmentation of Metaphase Images Containing Extrachromosomal DNA},
  author={Rajkumar, Utkrisht and Turner, Kristen and Luebeck, Jens and Deshpande, Viraj and Chandraker, Manmohan and Mischel, Paul and Bafna, Vineet},
  journal={iScience},
  volume={21},
  pages={428--435},
  year={2019},
  publisher={Elsevier}
}

@article{wu2019circular,
  title={Circular ecDNA promotes accessible chromatin and high oncogene expression},
  author={Wu, Sihan and Turner, Kristen M and Nguyen, Nam and Raviram, Ramya and Erb, Marcella and Santini, Jennifer and Luebeck, Jens and Rajkumar, Utkrisht and Diao, Yarui and Li, Bin and others},
  journal={Nature},
  volume={575},
  number={7784},
  pages={699--703},
  year={2019},
  publisher={Nature Publishing Group}
}

@article{luebeck2020ampliconreconstructor,
  title={AmpliconReconstructor: Integrated analysis of NGS and optical mapping resolves the complex structures of focal amplifications in cancer},
  author={Luebeck, Jens and Coruh, Ceyda and Dehkordi, Siavash R and Lange, Joshua T and Turner, Kristen M and Deshpande, Viraj and Pai, Dave A and Zhang, Chao and Rajkumar, Utkrisht and Law, Julie A and others},
  journal={bioRxiv},
  year={2020},
  publisher={Cold Spring Harbor Laboratory}
}

@article{rocca2020crispr,
  title={CRISPR/Cas9 gene editing of hematopoietic stem cells from patients with Friedreich’s ataxia},
  author={Rocca, Celine J and Rainaldi, Joseph N and Sharma, Jay and Shi, Yanmeng and Haquang, Joseph H and Luebeck, Jens and Mali, Prashant and Cherqui, Stephanie},
  journal={Molecular Therapy-Methods \& Clinical Development},
  year={2020},
  publisher={Elsevier}
}
