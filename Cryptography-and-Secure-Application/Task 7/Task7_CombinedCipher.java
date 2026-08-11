//java
import java.nio.file.Files;
import java.nio.file.Path;

public class Task7_CombinedCipher {

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

    // ===== 1-BIT CFB FOR A SINGLE BYTE =====
    static byte oneBitCFBByte(byte input, int[] SR, int[] key) {
        for (int i = 0; i < 8; i++) {
            int[] temp = {SR[0], SR[1]};
            encryptTEA(temp, key);

            int ksBit = (temp[0] >>> 31) & 1;
            int pBit = (input >>> (7 - i)) & 1;
            int cBit = pBit ^ ksBit;

            input &= ~(1 << (7 - i));
            input |= (cBit << (7 - i));

            SR[0] = (SR[0] << 1) | cBit;
        }
        return input;
    }

    // ===== SYNCHRONOUS CIPHER BYTE =====
    static byte syncByte(byte input, byte ks) {
        return (byte) (input ^ ks);
    }

    public static void main(String[] args) throws Exception {

        byte[] data = Files.readAllBytes(Path.of("bigfile.bin"));

        int[] teaKey = {1, 2, 3, 4};
        int[] SR = {0, 0};

        // Generate synchronous keystream
        byte[] ks = new byte[data.length];
        ks[0] = 3;
        ks[1] = 4;
        for (int i = 2; i < ks.length; i++) {
            ks[i] = (byte) (ks[i - 1] + ks[i - 2]);
        }

        // ENCRYPT
        long startEnc = System.nanoTime();
        for (int i = 0; i < data.length; i++) {
            if (i % 2 == 0) {
                data[i] = syncByte(data[i], ks[i]);
            } else {
                data[i] = oneBitCFBByte(data[i], SR, teaKey);
            }
        }
        long endEnc = System.nanoTime();

        // DECRYPT (same logic)
        SR[0] = SR[1] = 0;
        long startDec = System.nanoTime();
        for (int i = 0; i < data.length; i++) {
            if (i % 2 == 0) {
                data[i] = syncByte(data[i], ks[i]);
            } else {
                data[i] = oneBitCFBByte(data[i], SR, teaKey);
            }
        }
        long endDec = System.nanoTime();

        System.out.println("Combined cipher encryption time: "
                + (endEnc - startEnc) / 1_000_000.0 + " ms");
        System.out.println("Combined cipher decryption time: "
                + (endDec - startDec) / 1_000_000.0 + " ms");
    }
}
