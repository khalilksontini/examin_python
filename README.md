# Movie Actor Explorer - FAQ & Notes

---

## Question 1 : Pourquoi faut-il souvent committer le film (Movie) avant de créer les acteurs (Actors) ?

**Réponse :**

Parce que les *Actors* dépendent du `movie_id` qui est la clé primaire du film. Cette clé est générée automatiquement par la base de données lorsque le film est inséré (`db.commit()` + `db.refresh()`).

Sans cette clé, tu ne peux pas créer les acteurs correctement puisqu’il te manquerait la valeur de la clé étrangère `movie_id`.

---

## Question 2 : Lazy loading vs Eager loading dans SQLAlchemy

**Lazy loading (chargement paresseux) :**

Les relations (comme `movie.actors`) ne sont chargées que lorsqu’on y accède la première fois. Cela peut provoquer des requêtes SQL supplémentaires à la volée (problème des N+1 requêtes).

**Eager loading (chargement anticipé) avec `joinedload` :**

Les relations sont chargées immédiatement en même temps que la requête principale via une jointure SQL, ce qui évite les requêtes supplémentaires.

---

## Question 3 : How would you format the list of actors fetched from the database into a simple string suitable for inclusion in the LLM prompt?

- Use commas to separate actors for compactness.
- If the list is long, consider truncating or summarizing to avoid overloading the prompt.
- Avoid JSON or complex data structures inside prompts unless specifically needed.
- Make sure the formatting aligns with the style of the prompt so the LLM can parse it easily.

---
