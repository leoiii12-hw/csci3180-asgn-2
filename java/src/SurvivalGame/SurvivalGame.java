package SurvivalGame;

import java.util.Scanner;

public class SurvivalGame {
    public static Scanner reader = new Scanner(System.in);
    public final int D = 10; // dimension of board
    private final int O = 2; // Number of obstacles
    private int n; // Number of player
    private Object[] teleportObjects;

    public static void main(String[] args) {
        SurvivalGame game = new SurvivalGame();
        game.init();
        game.gameStart();
    }

    public void printBoard() {
        String printObject[][] = new String[D][D];

        // init printObject
        for (int i = 0; i < D; i++)
            for (int j = 0; j < D; j++)
                printObject[i][j] = "  ";

        for (int i = 0; i < n; i++) {
            Pos pos = ((Player) teleportObjects[i]).getPos();
            printObject[pos.getX()][pos.getY()] = ((Player) teleportObjects[i]).getName();
        }

        for (int i = n; i < n + O; i++) {
            Pos pos = ((Obstacle) teleportObjects[i]).getPos();
            printObject[pos.getX()][pos.getY()] = "O" + Integer.toString(i - n);
        }

        // printing
        System.out.print(" ");
        for (int i = 0; i < D; i++)
            System.out.print(String.format("| %d  ", i));

        System.out.println("|");

        for (int i = 0; i < D * 5.5; i++)
            System.out.print("-");
        System.out.println("");

        for (int row = 0; row < D; row++) {
            System.out.print(row);
            for (int col = 0; col < D; col++)
                System.out.print(String.format("| %s ",
                        printObject[row][col]));
            System.out.println("|");
            for (int i = 0; i < D * 5.5; i++)
                System.out.print("-");
            System.out.println("");
        }

        System.out.flush();
    }

    public boolean positionOccupied(int randx, int randy) {
        for (Object o : teleportObjects) {
            if (o instanceof Player) {
                Pos pos = ((Player) o).getPos();
                if (pos.getX() == randx && pos.getY() == randy)
                    return true;
            } else {
                Pos pos = ((Obstacle) o).getPos();
                if (pos.getX() == randx && pos.getY() == randy)
                    return true;
            }

        }

        return false;
    }

    public Player getPlayer(int randx, int randy) {
        for (Object o : teleportObjects) {
            if (o instanceof Player) {
                Pos pos = ((Player) o).getPos();
                if (pos.getX() == randx && pos.getY() == randy)
                    return (Player) o;
            }
        }

        return null;
    }

    private void init() {
        System.out.println("Welcome to Kafustrok. Light blesses you. \nInput number of players: (a even number)");
        n = reader.nextInt();

        teleportObjects = new Object[n + O];

        for (int i = 0; i < n / 2; i++) {
            Human human = new Human(0, 0, i, this);
            Chark chark = new Chark(0, 0, i, this);

            if (i == n / 2 - 1) {
                human.equip(new Wand(human));
                chark.equip(new Wand(chark));
            } else {
                human.equip(new Rifle(human));
                chark.equip(new Axe(chark));
            }

            teleportObjects[i] = human;
            teleportObjects[i + n / 2] = chark;
        }

        for (int i = 0; i < O; i++) {
            teleportObjects[i + n] = new Obstacle(0, 0, i, this);
        }
    }

    private void gameStart() {
        int turn = 0;

        while (true) {
            if (turn == 0) {
                for (Object obj : teleportObjects) {
                    if (obj instanceof Human)
                        ((Human) obj).teleport();
                    else if (obj instanceof Chark)
                        ((Chark) obj).teleport();
                    else if (obj instanceof Obstacle)
                        ((Obstacle) obj).teleport();
                }
                System.out.println("Everything gets teleported..");
            }

            printBoard();

            Player t = (Player) teleportObjects[turn];

            if (t.health > 0) {
                t.askForMove();
                System.out.println("\n");
            }

            turn = (turn + 1) % n;

            int numOfAliveHumans = 0;
            int numOfAliveCharks = 0;

            for (int i = 0; i < n; i++) {
                Object teleportObject = teleportObjects[i];

                if (teleportObject instanceof Human) {
                    if (((Human) teleportObject).health > 0) {
                        numOfAliveHumans += 1;
                    }
                }

                if (teleportObject instanceof Chark) {
                    if (((Chark) teleportObject).health > 0) {
                        numOfAliveCharks += 1;
                    }
                }
            }

            if (numOfAliveHumans == 0 || numOfAliveCharks == 0) {
                break;
            }
        }

        System.out.println("Game over.");
        printBoard();
    }
}
