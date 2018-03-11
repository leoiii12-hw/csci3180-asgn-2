package SurvivalGame;

public class Rifle extends Weapon {
    private static final int RIFLE_RANGE = 4;
    private static final int RIFLE_INIT_DAMAGE = 10;
    private static final int AMMO_LIMIT = 6;
    private static final int AMMO_RECHARGE = 3;

    private int ammo;

    public Rifle(Player owner) {
        super("Rifle", RIFLE_RANGE, RIFLE_INIT_DAMAGE, owner);

        this.ammo = AMMO_LIMIT;
    }

    @Override
    public void action(int posx, int posy) {
        System.out.println("You are using rifle attacking " + posx + " " + posy + ".");
        System.out.println("Type how many ammos you want to use.");

        int ammoToUse = SurvivalGame.reader.nextInt();

        if (ammoToUse > this.ammo) {
            System.out.println("You don't have that ammos.");
            return;
        }

        if (this.owner.pos.distance(posx, posy) <= this.range) {
            // search for all targets with target coordinates.
            Player player = owner.game.getPlayer(posx, posy);

            if (player != null) {
                if (!player.getRace().equals(this.owner.getRace())) {
                    player.decreaseHealth(this.effect * ammoToUse);
                    ammo -= ammoToUse;
                } else {
                    System.out.println("No cannibalism.");
                }
            }
        } else
            System.out.println("Out of reach.");
    }

    @Override
    public void enhance() {
        this.ammo = Math.min(AMMO_LIMIT, this.ammo + AMMO_RECHARGE);
    }

    public String getDetails() {
        return String.format(
                "(Range %d, Ammo #: %d, Damage per shot: %d)",
                this.getRange(),
                this.getAmmo(),
                this.getEffect());
    }

    public int getAmmo() {
        return this.ammo;
    }

}
