2025-10-18 22:58

Status: #Ongoing

Tags: [[Natural Language Processing]]
***
# Definitions

- **Corpus (pl. corpora).** Refers to a set of data, carefully collected, sometimes annotated and/or curated.
- **Documents/Instances.** The elements that make up a corpus are known as documents or instances.
	- If we wanted to draw a parallel with the datasets we generally use in ML, a document is equivalent to an observation.
- **Vocabulary.** When we talk about vocabulary, we refer to all the words (without duplicates) that we can find in our corpus. We define $|V|$ as the size of the vocabulary.
- **Words.** Defining what a word is is a very difficult task because it depends on the task we are trying to develop. Some factors that contribute to making this task so difficult are:
	- Punctuation marks such as the period (`.`) and comma (`,`) are usually very useful for determining word boundaries, but depending on the task we are working on, it may be convenient to consider these punctuation marks as words.
	- In corpora containing text from conversations, which often introduce **fragments** of words (e.g., when we say *"por?"* instead of saying *"por qué?"*) or **fillers** (e.g., when between words we say *"ehhh"*), we have to decide whether to consider them as words or not. This will depend on the task we are working on (e.g., in *speech recognition* tasks they are usually considered words because they help us predict the next word in the conversation, but in tasks like *machine translation* they are not).

# Text Normalization

## Tokenization

- It is a process that consists of separating texts into individual units known as **tokens**.
- Tokens can represent several things: a word, a letter, a morpheme, a syllable, a phrase, etc. That depends on the task we are working on.
- There are many ways to tokenize a text. Which one we use depends on the task we are performing.
	- **Word Tokenization.** Divides the text into individual words. It is usually very useful for analyzing the sentiment of a text or for generating summaries.
	- **Character Tokenization.** Divides the text into characters. It is often used for text correction or for language models (for languages with complex morphologies).
	- **Sub-word Tokenization.** Divides the text into words or morphemes. It is often used by models like BERT, because from these tokens they can build words that are not found in the training vocabulary.
		- For example, a model trained with a Spanish corpus may not have encountered the word "*boludo*" that we Argentines use during training. However, it could construct that word from the tokens in its training vocabulary.
		- It is also very useful for reducing the size of vocabularies.
	- **Sentence Tokenization.** Divides the text into shorter phrases or sentences.
	- **N-gram Tokenization.** The tokens are sequences of $N$ words. Very useful when you want to capture the context in which it is used.
- We also have many types of tokenizers:
	- **Ruled-based Tokenization.** Uses a set of pre-defined rules to separate the text into tokens. For example, it could use white spaces to separate words (tokens).
	- **Statistical Tokenization.** Uses statistical models to define the boundary between two tokens.
		- It is often very useful for languages like Japanese or Chinese, which do not use white spaces to separate words.
		- They depend on how well trained the models are.
	- **Byte-Pair Encoding (BPE).** Starts from a vocabulary where each character is a token. From that vocabulary, it combines characters based on their frequency.
		- Widely used by language models (LLMs) because it solves the problem of words not found in the vocabulary (OOV).
	- **ML-based Tokenization.** Uses ML algorithms to learn rules from annotations in texts. These methods are very flexible and can be used for multiple languages.

# References
- (2024, June 25) *What is Tokenization in Natural Language Processing (NLP)?*. GeeksforGeeks. [URL](https://www.geeksforgeeks.org/tokenization-in-natural-language-processing-nlp/).
- (2024, November 15) *Mastering Tokenization in NLP: An In-Depth Look at Methods, Types, and Challenges*. Calibrant. [URL](https://www.calibraint.com/blog/understanding-tokenization-in-nlp-guide).