# Understanding LLMs

## What is an LLM?

A neural network trained on massive amounts of text (often large portions of the public internet) to understand, generate, and respond to human-like text.

## Stages of Building an LLM

Pretraining: trained on next-word prediction over large unlabeled text corpora. This produces a base or foundation model, like GPT-3.

- Capable of text completion
- Limited few-shot ability (can learn new tasks from just a few examples)

Fine-tuning: further training on smaller, labeled datasets. Two main types:

| Type                       | Data format                  | Example                                                   |
| -------------------------- | ---------------------------- | --------------------------------------------------------- |
| Instruction fine-tuning    | Instruction and answer pairs | "Translate this text" paired with the correct translation |
| Classification fine-tuning | Text and class label         | Email labeled "spam" or "not spam"                        |

## The Transformer Architecture

Two submodules:

- Encoder: processes input text into numerical vectors or contextual representations
- Decoder: takes those vectors and generates output text

Both are built from stacked layers connected by self-attention, a mechanism that lets the model weigh how relevant each word or token is to every other word in a sequence. This is what captures long-range dependencies and context and it's why the output ends up coherent.

Two notable variants:

| Model                                                          | Uses         | Specializes in                                                                                                                 |
| -------------------------------------------------------------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------ |
| BERT (Bidirectional Encoder Representations from Transformers) | Encoder only | Masked word prediction, strong at classification tasks like sentiment analysis, document categorization, toxicity detection    |
| GPT (Generative Pretrained Transformer)                        | Decoder only | Text generation: translation, summarization, fiction, code. Strong at zero-shot (unseen tasks, no examples) and few-shot tasks |

Transformers and LLMs aren't quite synonyms:

- Not all transformers are LLMs (vision transformers work on images, for instance)
- Not all LLMs are transformers, since some use recurrent or convolutional architectures instead, usually for better computational efficiency

## The GPT Architecture

- Decoder-only, no encoder submodule
- Autoregressive: generates one word at a time and feeds its own prior outputs back in as input for the next prediction, which is part of what keeps the output coherent
- Scale: the original transformer repeated its encoder and decoder blocks six times. GPT-3 has 96 transformer layers and 175 billion parameters

## GPT-3 Pretraining Data

| Dataset name           | Description                | Tokens      | % of training data |
| ---------------------- | -------------------------- | ----------- | ------------------ |
| CommonCrawl (filtered) | Web crawl data             | 410 billion | 60%                |
| WebText2               | Web crawl data             | 19 billion  | 22%                |
| Books1                 | Internet-based book corpus | 12 billion  | 8%                 |
| Books2                 | Internet-based book corpus | 55 billion  | 8%                 |
| Wikipedia              | High-quality text          | 3 billion   | 3%                 |

Notes:

- The token subsets above add up to roughly 499 billion, but GPT-3 was actually trained on only 300 billion tokens. The original paper doesn't explain the gap.
- CommonCrawl alone requires about 570 GB of storage.
- Later models expanded on this. Meta's LLaMA, for example, added Arxiv papers (92 GB) and StackExchange Q&A (78 GB) as additional sources.

## Key Takeaways

- LLMs replaced older rule-based and statistical NLP methods with deep learning, improving how machines understand, generate, and translate language.
- Training happens in two stages: pretraining on next-word prediction over unlabeled text, then fine-tuning on labeled data for instructions or classification.
- The transformer's core innovation is self-attention, which gives the model selective access to the full input sequence at each step of generation.
- The original transformer paired an encoder for parsing text with a decoder for generating it. Generative LLMs like GPT and ChatGPT simplify this by using decoder-only architectures.
- Pretraining requires massive datasets, often billions of tokens.
- Even though LLMs are only trained to predict the next word, they show emergent abilities: classification, translation, summarization, and more.
- Once pretrained, a foundation model can be fine-tuned efficiently for many downstream tasks.
- Domain-specific fine-tuned LLMs can outperform general-purpose LLMs on specialized tasks.

## References

- Wu et al. (2023). BloombergGPT: A Large Language Model for Finance. GPT pretrained from scratch on finance data, outperformed ChatGPT on financial tasks. https://arxiv.org/abs/2303.17564
- Singhal et al. (2023). Towards Expert-Level Medical Question Answering with Large Language Models (Google Research/DeepMind). Fine-tuning existing LLMs for medical use. https://arxiv.org/abs/2305.09617
- Vaswani et al. (2017). Attention Is All You Need. The original transformer architecture. https://arxiv.org/abs/1706.03762
- Devlin et al. (2018). BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. https://arxiv.org/abs/1810.04805
- Brown et al. (2020). Language Models are Few-Shot Learners. The GPT-3 paper. https://arxiv.org/abs/2005.14165
- Dosovitskiy et al. (2020). An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale. The vision transformer. https://arxiv.org/abs/2010.11929
- Touvron et al. (2023). Llama 2: Open Foundation and Fine-Tuned Chat Models (Meta AI). https://arxiv.org/abs/2307.09288
- Gao et al. (2020). The Pile: An 800GB Dataset of Diverse Text for Language Modeling (EleutherAI). https://arxiv.org/abs/2101.00027
- Ouyang et al. (2022). Training Language Models to Follow Instructions with Human Feedback. The InstructGPT paper. https://arxiv.org/abs/2203.02155
