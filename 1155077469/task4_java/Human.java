

public class Human extends Player {

    public Human(int posx, int posy, int index, SurvivalGame game) {
        super(80, 2, posx, posy, index, game, "Human");
    }

    public void teleport() {
        super.teleport();

        if (equipment instanceof Weapon)
            ((Weapon) this.equipment).enhance();
        if (equipment instanceof Wand)
            ((Wand) this.equipment).enhance();
    }

    @Override
    public void askForMove() {
        Weapon weapon = null;
        Wand wand = null;

        if (equipment instanceof Weapon)
            weapon = (Weapon) this.equipment;
        if (equipment instanceof Wand)
            wand = (Wand) this.equipment;

        System.out.println(String.format(
                "You are a human (H%d) using %s. %s",
                this.index,
                weapon != null ? weapon.getName() : (wand != null ? wand.getName() : null),
                weapon != null ? weapon.getDetails() : (wand != null ? wand.getDetails() : null)));

        super.askForMove();

    }

}
