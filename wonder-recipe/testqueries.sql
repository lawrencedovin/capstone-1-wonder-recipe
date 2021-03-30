SELECT r.recipe_name, c.cuisine_name
    FROM recipes r
    JOIN cuisines c
        ON r.cuisine_id = c.id;

SELECT r.recipe_name, d.diet_name
    FROM recipe_diet rd
    JOIN recipes r
        ON r.id = rd.recipe_id
    JOIN diets d
        ON d.id = rd.diet_id;

SELECT u.username, r.recipe_name
    FROM grocery_list gl
    JOIN users u
        ON u.id = gl.user_id
    JOIN recipes r
        ON r.id = gl.recipe_id;