
# Task 3 — Mathematical Analysis of a Proposed Substitution Cipher

Mathematical proof analyzing whether the function `f(x) = x^k mod 26` (for key `k > 1`) can serve as a valid substitution cipher.

## 📋 Problem

Letters are mapped to integers 0–25 (A=0, ..., Z=25) and "encrypted" using:

f(x) = x^k (mod 26), where k > 1


**Question:** can this function be used as a valid substitution cipher?

## 📐 Requirement for a Valid Substitution Cipher

For any substitution cipher to be valid, its encryption function must be **one-to-one (injective)** — every plaintext letter must map to a *unique* ciphertext letter, so that decryption (recovering the unique original plaintext letter from a given ciphertext letter) is possible.

## 🔍 Analysis

**26 is composite:** `26 = 2 × 13`

Because the modulus is composite (not prime), exponentiation modulo 26 does **not** produce a permutation of the alphabet — the function is not guaranteed to be one-to-one.

**Counter-example (k = 2):**

f(2) = 2² = 4 ≡ 4 (mod 26)
f(24) = 24² = 576 ≡ 4 (mod 26)


Two different plaintext letters (`2` and `24`, i.e. 'C' and 'Y') both map to the same ciphertext value (`4`, i.e. 'E') — making `f` non-invertible for this input: given ciphertext letter 'E', there is no way to determine whether the original plaintext letter was 'C' or 'Y'.

**This is not an isolated case.** Computing `f(x) = x² mod 26` across the full alphabet reveals the collision problem is systemic, not a one-off coincidence:

f({1, 25}) = 1
f({9, 17}) = 3
f({2, 24}) = 4
f({3, 23}) = 9
f({6, 20}) = 10
f({8, 18}) = 12
f({12, 14}) = 14
f({4, 22}) = 16
f({11, 15}) = 17
f({10, 16}) = 22
f({7, 19}) = 23
f({5, 21}) = 25


**12 separate collision pairs** exist for k=2 alone — meaning only **14 of the 26 possible output values** are ever produced. More than half the alphabet's ciphertext space is wasted, and every one of those 12 output values is ambiguous between two possible plaintext letters.

## ✅ Conclusion

Since `f(x) = x^k mod 26` is not one-to-one for `k > 1` (a direct consequence of 26 being composite), it **cannot be used as a valid substitution cipher** — encryption would be irreversible for any input landing in a collision pair, making correct decryption impossible in general.

## 🎯 Relevance to Blue Team / Security

This proof illustrates a fundamental requirement for any cryptographic transformation intended to be reversible: the underlying function must be a true permutation (bijection) over its domain. Recognizing when a proposed "encryption" scheme fails this property — often due to a poorly chosen modulus, as with composite 26 here — is directly relevant to identifying broken or non-invertible custom encoding schemes sometimes encountered in real systems (e.g. flawed obfuscation or "encryption" implementations that silently produce collisions and data loss).
