SELECT r.title as recipe, c.title as cuisine
    FROM recipes r
    JOIN cuisines c
        ON r.cuisine_id = c.id;

SELECT r.title as recipe, d.title as diet
    FROM recipe_diet rd
    JOIN recipes r
        ON r.id = rd.recipe_id
    JOIN diets d
        ON d.id = rd.diet_id;

SELECT r.title as recipe, c.title as cuisine
    FROM recipe_cuisine rc
    JOIN recipes r
        ON r.id = rc.recipe_id
    JOIN cuisines c
        ON c.id = rc.cuisine_id;

SELECT u.username as user, r.recipe_name as recipe
    FROM grocery_list gl
    JOIN users u
        ON u.id = gl.user_id
    JOIN recipes r
        ON r.id = gl.recipe_id;

SELECT u.username as user, r.recipe_name as recipe
    FROM likes lr
    JOIN users u
        ON u.id = lr.user_id
    JOIN recipes r
        ON r.id = lr.recipe_id;