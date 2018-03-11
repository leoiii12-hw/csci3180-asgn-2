package SurvivalGame;

public class Wand {
    private final String name;
    protected final int range;
    protected int effect;
    protected Player owner;

    protected Wand(Player owner) {
        this.name = "Wand";
        this.range = 5;
        this.effect = 5;
        this.owner = owner;
    }

    public void action(int posx, int posy) {
        System.out.println(String.format("You are using wand healing %d %d.", posx, posy));

        if (this.owner.pos.distance(posx, posy) <= this.range) {
            // search for all targets with target coordinates.
            Player player = owner.game.getPlayer(posx, posy);

            if (player != null) {
                if (player.getRace().equals(this.owner.getRace())) {
                    player.increaseHealth(this.effect);
                } else {
                    System.out.println("No other race healing.");
                }
            }
        } else {
            System.out.println("Out of reach.");
        }
    }

    public void enhance() {
        this.effect += 5;
    }

    public int getEffect() {
        return this.effect;
    }

    public int getRange() {
        return this.range;
    }

    public String getName() {
        return this.name;
    }

    public String getDetails() {
        return String.format("(Range: %d, Healing effect: %d)", this.getRange(), this.getEffect());
    }
}
