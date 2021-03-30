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