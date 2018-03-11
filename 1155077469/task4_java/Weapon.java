

public abstract class Weapon {
    private final String name;
    protected final int range;
    protected int effect;
    protected Player owner;

    protected Weapon(String name, int range, int damage, Player owner) {
        this.name = name;
        this.range = range;
        this.effect = damage;
        this.owner = owner;
    }

    abstract public void action(int posx, int posy);

    abstract public void enhance();

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
        return null;
    }
}
