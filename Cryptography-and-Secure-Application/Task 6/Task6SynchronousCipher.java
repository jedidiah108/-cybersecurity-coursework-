//java
public class Task6SynchronousCipher {

    // Map A–Z to 0–25
    static int charToInt(char c) {
        return c - 'A';
    }

    // Map 0–25 back to A–Z
    static char intToChar(int i) {
        return (char) ('A' + i);
    }

    // Generate keystream
    static int[] generateKeystream(int key, int length) {
        int[] k = new int[length];
        k[0] = key % 26;
        if (length > 1) {
            k[1] = (key + 1) % 26;
        }
        for (int i = 2; i < length; i++) {
            k[i] = (k[i - 1] + k[i - 2]) % 26;
        }
        return k;
    }

    // Encrypt
    static String encrypt(String plaintext, int key) {
        plaintext = plaintext.replace(" ", "").toUpperCase();
        int[] keystream = generateKeystream(key, plaintext.length());
        StringBuilder cipher = new StringBuilder();

        for (int i = 0; i < plaintext.length(); i++) {
            int m = charToInt(plaintext.charAt(i));
            int c = (m + keystream[i]) % 26;
            cipher.append(intToChar(c));
        }
        return cipher.toString();
    }

    // Decrypt
    static String decrypt(String ciphertext, int key) {
        ciphertext = ciphertext.toUpperCase();
        int[] keystream = generateKeystream(key, ciphertext.length());
        StringBuilder plain = new StringBuilder();

        for (int i = 0; i < ciphertext.length(); i++) {
            int c = charToInt(ciphertext.charAt(i));
            int m = (c - keystream[i] + 26) % 26;
            plain.append(intToChar(m));
        }
        return plain.toString();
    }

    public static void main(String[] args) {

        System.out.println("Encryption:");
        System.out.println(encrypt("I LOVE WOLLONGONG", 3));

        System.out.println("Decryption:");
        System.out.println(decrypt("MQJJ", 3));
    }
}
