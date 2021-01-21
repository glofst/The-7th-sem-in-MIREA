package ru.mirea;

public class MyHashFunction {

    private static final char [] alphabet = new char[]{
            'а','б','в','г','д','е','ё','ж',
            'з','и','й','к','л','м','н','о',
            'п','р','с','т','у','ф','х','ц',
            'ч','ш','щ','ъ','ы','ь','э','ю','я'
    };

    public static void main(String[] args) {
        System.out.println(HashFunction("угу ага ада омо сто ост сон нос"));
    }

    private static String HashFunction(String input) {
        StringBuilder hash = new StringBuilder();
        input = input.toLowerCase();
        String [] words = input.split(" ");

        for(String word : words) {
            int result = 0;
            for(int i = 0;i < word.length();i++) {
                result += (word.charAt(i) % (new String(alphabet).indexOf(word.charAt(i)) + 1)) * (i + 1);
                System.out.println(word.charAt(i) + ": " + (int) word.charAt(i) + ", " + result);
            }
            System.out.println();
            hash.append(result).append(" ");
        }

        return hash.toString();
    }
}
