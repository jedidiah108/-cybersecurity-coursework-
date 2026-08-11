//java
//just implement to 1-bit, the rest the same as task 5
import java.nio.file.Files;
import java.nio.file.Path;

public class Task7_OneBitCFB {

    // ===== TEA ENCRYPTION =====
    static void encryptTEA(int[] v, int[] k) {
        int v0 = v[0], v1 = v[1];
        int sum = 0;
        int delta = 0x9e3779b9;

        for (int i = 0; i < 32; i++) {
            sum += delta;
            v0 += ((v1 << 4) + k[0]) ^ (v1 + sum) ^ ((v1 >>> 5) + k[1]);
            v1 += ((v0 << 4) + k[2]) ^ (v0 + sum) ^ ((v0 >>> 5) + k[3]);
        }

        v[0] = v0;
        v[1] = v1;
    }

    // ===== 1-BIT CFB ENCRYPT =====
    static void encrypt1BitCFB(byte[] data) {
        int[] SR = {0, 0};        // shift register (IV)
        int[] key = {1, 2, 3, 4};

        int bitPos = 0;
        int totalBits = data.length * 8;

        while (bitPos < totalBits) {
            int[] temp = {SR[0], SR[1]};
            encryptTEA(temp, key);

            int ksBit = (temp[0] >>> 31) & 1;

            int byteIndex = bitPos / 8;
            int bitIndex = 7 - (bitPos % 8);
            int pBit = (data[byteIndex] >>> bitIndex) & 1;

            int cBit = pBit ^ ksBit;

            // write ciphertext bit back
            data[byteIndex] &= ~(1 << bitIndex);
            data[byteIndex] |= (cBit << bitIndex);

            SR[0] = (SR[0] << 1) | cBit;
            bitPos++;
        }
    }

    // ===== 1-BIT CFB DECRYPT =====
    static void decrypt1BitCFB(byte[] data) {
        int[] SR = {0, 0};        // same IV
        int[] key = {1, 2, 3, 4};

        int bitPos = 0;
        int totalBits = data.length * 8;

        while (bitPos < totalBits) {
            int[] temp = {SR[0], SR[1]};
            encryptTEA(temp, key);

            int ksBit = (temp[0] >>> 31) & 1;

            int byteIndex = bitPos / 8;
            int bitIndex = 7 - (bitPos % 8);
            int cBit = (data[byteIndex] >>> bitIndex) & 1;

            int pBit = cBit ^ ksBit;

            // write plaintext bit back
            data[byteIndex] &= ~(1 << bitIndex);
            data[byteIndex] |= (pBit << bitIndex);

            SR[0] = (SR[0] << 1) | cBit;
            bitPos++;
        }
    }

    public static void main(String[] args) throws Exception {

        byte[] fileData = Files.readAllBytes(Path.of("bigfile.bin"));

        // ENCRYPT
        long startEnc = System.nanoTime();
        encrypt1BitCFB(fileData);
        long endEnc = System.nanoTime();

        // DECRYPT
        long startDec = System.nanoTime();
        decrypt1BitCFB(fileData);
        long endDec = System.nanoTime();

        System.out.println("1-bit CFB encryption time: "
                + (endEnc - startEnc) / 1_000_000.0 + " ms");
        System.out.println("1-bit CFB decryption time: "
                + (endDec - startDec) / 1_000_000.0 + " ms");
    }
}

