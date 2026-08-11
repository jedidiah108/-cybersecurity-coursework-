# Task 2 — Keyword-Based Substitution Cipher (Java)

Java implementation of a classical monoalphabetic substitution cipher, where the substitution key is derived from a chosen keyword rather than a random permutation.

## 📋 Overview

The cipher builds its 26-letter substitution alphabet from a keyword:

1. Duplicate letters in the keyword are removed, preserving first-occurrence order
2. The remaining (unused) letters of the alphabet are appended in **reverse order** (Z to A)
3. The resulting 26-letter sequence becomes the substitution key — plaintext letter at position `n` (A=0, B=1, ...) maps to the key's letter at position `n`

Encryption substitutes each plaintext letter with its corresponding key letter; decryption reverses the lookup. Case is preserved in the output, and non-alphabetic characters (numbers, punctuation, spaces) pass through unchanged.

## 🔑 Worked Example

Using the keyword **`STRAWBERRY`**:

**Step 1 — build the key:**
Unique letters from the keyword (duplicates removed): `S T R A W B E Y`
Remaining alphabet appended Z→A: `Z X V U Q P O N M L K J I H G F D C`

**Resulting key:**
Plain: A B C D E F G H I J K L M N O P Q R S T U V W X Y Z

Key: S T R A W B E Y Z X V U Q P O N M L K J I H G F D C

**Step 2 — encrypt/decrypt a sample sentence:**

Plaintext:

this is the test for assignment1 task 2, just writing anything to make it like a paragraph, but I only can able to write a sentence somehow.

Ciphertext:

jyzk zk jyw jwkj bol skkzepqwpj1 jskv 2, xikj glzjzpe spdjyzpe jo qsvw zj uzvw s nslselsny, tij Z opud rsp stuw jo glzjw s kwpjwprw koqwyog.

Decrypting the ciphertext with the same keyword reproduces the original plaintext exactly, confirming correct round-trip behavior. Notice that numbers (`1`, `2`), punctuation (`,`, `.`), spaces, and case are all preserved unchanged — only alphabetic characters are substituted.

## ▶️ Usage

**Compile:**
```bash
javac SubstitutionCipher.java
```

**Encrypt:**
```bash
java SubstitutionCipher enc STRAWBERRY plaintext.txt ciphertext.txt
```

**Decrypt:**
```bash
java SubstitutionCipher dec STRAWBERRY ciphertext.txt decrypted.txt
```

`decrypted.txt` will match the original `plaintext.txt` exactly.

## 🛠️ Files

- **`SubstitutionCipher.java`** — cipher implementation (key generation, encrypt, decrypt)
- **`plaintext.txt`** — sample input file used for testing

## 🎯 Relevance to Blue Team / Security

Implementing a classical cipher from scratch reinforces understanding of how monoalphabetic substitution works structurally — directly useful when analyzing or reverse-engineering weak/homegrown obfuscation schemes encountered in real investigations, and builds the foundation for recognizing why keyword-derived keys (as opposed to fully random permutations) can reduce the effective keyspace an attacker needs to search.
