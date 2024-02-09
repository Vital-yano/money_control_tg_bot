from redis.commands.search.field import TextField

redis_schema = (
    TextField("$.tg_id", as_name="tg_id"),
    TextField("$.tg_nickname", as_name="tg_nickname"),
    TextField("$.phone_number", as_name="phone_number"),
    TextField("$.verification_code", as_name="code"),
    TextField("$.registration_time", as_name="registration_time"),
)
