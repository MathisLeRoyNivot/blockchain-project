CREATE TABLE "users" (
  "id" SERIAL PRIMARY KEY,
  "full_name" varchar,
  "created_at" timestamp
);

CREATE TABLE "block" (
  "id" SERIAL PRIMARY KEY,
  "block_code" int,
  "nonce" int,
  "hash_code" varchar,
  "previous_hash_code" varchar,
  "timestamp" int,
  "user_id" int
);

CREATE TABLE "pages" (
  "id" SERIAL PRIMARY KEY,
  "pages_code" varchar,
  "hash_code" varchar,
  "previous_hash_code" varchar,
  "block_id" varchar
);

CREATE TABLE "chaine" (
  "block_id" varchar,
  "user_id" int
);

ALTER TABLE "block" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "pages" ADD FOREIGN KEY ("block_id") REFERENCES "block" ("id");

ALTER TABLE "chaine" ADD FOREIGN KEY ("block_id") REFERENCES "block" ("id");

ALTER TABLE "chaine" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");
