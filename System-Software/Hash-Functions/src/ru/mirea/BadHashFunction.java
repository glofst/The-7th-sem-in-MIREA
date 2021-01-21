package ru.mirea;

public class BadHashFunction {

        private static final char [] alphabet = new char[]{
                'а','б','в','г','д','е','ё','ж',
                'з','и','й','к','л','м','н','о',
                'п','р','с','т','у','ф','х','ц',
                'ч','ш','щ','ъ','ы','ь','э','ю','я'
        };

        public static void main(String[] args) {
            System.out.println(HashFunc("угу,ага,омо,сто,ост,сон,нос"));
        }

        public static String HashFunc(String input){
            StringBuilder hash = new StringBuilder();
            int sum = 0, first=0, last=0;
            input = input.toLowerCase();
            String [] words = input.split("\\s|[.!,?\\-]");

            for (String word : words) {
                for (int j = 0; j < word.length(); j++) {
                    for (int k = 0; k < alphabet.length; k++) {
                        if (word.charAt(0) == alphabet[k])
                            first = k;

                        if (word.charAt(word.length() - 1) == alphabet[k])
                            last = k + 1;

                        if (word.charAt(j) == alphabet[k])
                            sum += k;
                    }
                }
                sum = sum * ((last - first));
                hash.append(sum).append(" ");
                sum = 0;

            }

            return hash.toString();
        }

}

