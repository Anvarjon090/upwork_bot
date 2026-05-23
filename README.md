# upwork_bot

## Database

- Bot ishga tushganda `database.migrate.apply_migrations()` avtomatik ishlaydi.
- Migratsiyani qo'lda ishga tushirish uchun:

```bash
python -m database.migrate
```

- Hozirgi birinchi migratsiya `sent_jobs` jadvalini yaratadi va yuborilgan ishlarni saqlaydi.
