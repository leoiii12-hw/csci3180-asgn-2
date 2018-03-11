package SurvivalGame;

public class Axe extends Weapon {
    private static final int AXE_RANGE = 1;
    private static final int AXE_INIT_DAMAGE = 40;

    public Axe(Player owner) {
        super("Axe", AXE_RANGE, AXE_INIT_DAMAGE, owner);
    }

    @Override
    public void action(int posx, int posy) {
        System.out.println("You are using axe attacking " + posx + " " + posy + ".");

        if (this.owner.pos.distance(posx, posy) <= this.range) {
            // search for all targets with target coordinates.
            Player player = owner.game.getPlayer(posx, posy);

            if (player != null) {
                if (!player.getRace().equals(this.owner.getRace())) {
                    player.decreaseHealth(this.effect);
                } else {
                    System.out.println("No cannibalism.");
                }
            }
        } else {
            System.out.println("Out of reach.");
        }
    }

    public void enhance() {
        this.effect += 10;
    }

    @Override
    public String getDetails() {
        return String.format(
                "(Range: %d, Damage: %d)",
                this.getRange(),
                this.getEffect());
    }

}
