(() => {
  'use strict';
  const dictionaries = {
    uz: {},
    ru: {
      'Kirish':'Войти','Ro‘yxatdan o‘tish':'Регистрация','Yana xush kelibsiz':'С возвращением',
      'Hisobingizga kirish uchun ma’lumotlarni kiriting.':'Введите данные для входа в аккаунт.',
      'Email manzil':'Электронная почта','Parol':'Пароль','Parolingiz':'Ваш пароль',
      'Parolni unutdingizmi?':'Забыли пароль?','Yangi hisob yarating':'Создайте аккаунт',
      'Kissa bilan moliyangizni boshqarishni boshlang.':'Начните управлять финансами с Kissa.',
      'Ism':'Имя','Ismingiz':'Ваше имя','Familiya':'Фамилия','Familiangiz':'Ваша фамилия',
      'Foydalanuvchi nomi':'Имя пользователя','Parolni takrorlang':'Повторите пароль',
      'Kamida 8 belgi':'Не менее 8 символов','Til':'Язык','O‘zbek':'Узбекский',
      'Hisob yaratish':'Создать аккаунт','Emailni tasdiqlang':'Подтвердите email',
      'Emailingizga yuborilgan 6 xonali kodni kiriting.':'Введите 6-значный код из письма.',
      'Tasdiqlash kodi':'Код подтверждения','Tasdiqlash':'Подтвердить','Kodni qayta yuborish':'Отправить код повторно',
      'Parolni tiklash':'Восстановление пароля','Emailingizga kod yuboramiz.':'Отправим код на вашу почту.',
      'Kod yuborish':'Отправить код','Kirishga qaytish':'Вернуться ко входу',
      'Ma’lumotlaringiz faqat sizga tegishli.':'Ваши данные доступны только вам.',
      'SHAXSIY MOLIYA':'ЛИЧНЫЕ ФИНАНСЫ','Pulingizni':'Управляйте','ongli boshqaring.':'деньгами осознанно.',
      'Kirim, chiqim va maqsadlaringizni bitta sokin, tartibli makonda kuzating.':'Следите за доходами, расходами и целями в одном удобном месте.',
        'Har bir so‘m':'Каждый рубль','o‘z o‘rnida':'на своём месте','Moliyaviy':'Финансовая','aniqlik':'ясность',
      'Umumiy ko‘rinish':'Обзор','Tranzaksiyalar':'Транзакции','Hisoblar':'Счета','Kategoriyalar':'Категории',
      'MENYU':'МЕНЮ','Bugungi moliyaviy holatingizga bir nazar.':'Взгляните на своё финансовое состояние.',
      'Kirim va chiqimlaringizni kuzating.':'Следите за доходами и расходами.',
      'Pul saqlanadigan hisoblaringiz.':'Ваши денежные счета.','Tranzaksiyalaringizni tartibga soling.':'Упорядочите свои транзакции.',
      'Umumiy balans':'Общий баланс','Jami kirim':'Всего доходов','Jami chiqim':'Всего расходов',
      'Yangi tranzaksiya':'Новая транзакция','Tranzaksiya qo‘shish':'Добавить транзакцию',
      'Hisob qo‘shish':'Добавить счёт','Kategoriya qo‘shish':'Добавить категорию',
      'Hisoblaringiz':'Ваши счета','Naqd pul, karta va valyuta hisoblari':'Наличные, карты и валютные счета',
      'Chiqim kategoriyalari':'Категории расходов','Kirim kategoriyalari':'Категории доходов',
      'Sarflaringizni guruhlang':'Группируйте расходы','Daromad manbalari':'Источники дохода',
      'Barcha turlar':'Все типы','Barcha hisoblar':'Все счета','Kirim':'Доход','Chiqim':'Расход',
      'TRANZAKSIYA':'ТРАНЗАКЦИЯ','HISOB':'СЧЁТ','KATEGORI':'КАТЕГОРИЯ','SANA':'ДАТА','SUMMA':'СУММА',
      'Saqlash':'Сохранить','Bekor qilish':'Отмена','Yopish':'Закрыть','Yangi':'Новая',
      'Hisob nomi':'Название счёта','Hisob turi':'Тип счёта','Naqd pul':'Наличные','Bank kartasi':'Банковская карта',
      'Valyuta':'Валюта','Kategoriya nomi':'Название категории','Kategoriya turi':'Тип категории',
      'Tranzaksiya turi':'Тип транзакции','Hisob':'Счёт','Kategoriya':'Категория','Summa':'Сумма',
      'Sana':'Дата','Izoh':'Комментарий','Masalan, tushlik...':'Например, обед...',
      'Tahrirlash':'Изменить','O‘chirish':'Удалить','Yangilash':'Обновить','Hisob yaratish':'Создать счёт',
      'Muvaffaqiyatli saqlandi.':'Успешно сохранено.','Ma’lumot yangilandi.':'Данные обновлены.',
      'Sessiya tugadi. Qayta kiring.':'Сессия завершена. Войдите снова.',
      'Email yoki parol noto‘g‘ri.':'Неверный email или пароль.','Foydalanuvchi':'Пользователь','Chiqish':'Выйти',
      'Oldingi':'Назад','Keyingi':'Далее','sahifa':'страница','Yaratilgan:':'Создано:',
      'Hozircha ma’lumot yo‘q':'Пока нет данных','Kategoriya yo‘q.':'Категорий нет.',
      'Hali hisob yaratilmagan.':'Счёт ещё не создан.','Hisoblar hali yo‘q. Birinchi hisobingizni qo‘shing.':'Счетов пока нет. Добавьте первый счёт.',
      'Bu filtrda tranzaksiya topilmadi.':'По этому фильтру транзакций не найдено.',
      'Avval hisob yarating, keyin tranzaksiya qo‘shishingiz mumkin.':'Сначала создайте счёт, затем добавьте транзакцию.',
        'Avval kirim yoki chiqim kategoriyasini yarating.':'Сначала создайте категорию дохода или расхода.',
        'Kategoriyani tahrirlash':'Изменить категорию','Hisobni tahrirlash':'Изменить счёт',
        'Tranzaksiyani tahrirlash':'Изменить транзакцию','O‘zgarishlarni saqlash':'Сохранить изменения',
        'Hisob o‘chirildi.':'Счёт удалён.','Kategoriya o‘chirildi.':'Категория удалена.','Tranzaksiya o‘chirildi.':'Транзакция удалена.'
    },
    en: {
      'Kirish':'Log in','Ro‘yxatdan o‘tish':'Sign up','Yana xush kelibsiz':'Welcome back',
      'Hisobingizga kirish uchun ma’lumotlarni kiriting.':'Enter your account details to log in.',
      'Email manzil':'Email address','Parol':'Password','Parolingiz':'Your password',
      'Parolni unutdingizmi?':'Forgot password?','Yangi hisob yarating':'Create a new account',
      'Kissa bilan moliyangizni boshqarishni boshlang.':'Start managing your finances with Kissa.',
      'Ism':'First name','Ismingiz':'Your first name','Familiya':'Last name','Familiangiz':'Your last name',
      'Foydalanuvchi nomi':'Username','Parolni takrorlang':'Confirm password','Kamida 8 belgi':'At least 8 characters',
      'Til':'Language','O‘zbek':'Uzbek','Hisob yaratish':'Create account','Emailni tasdiqlang':'Verify your email',
      'Emailingizga yuborilgan 6 xonali kodni kiriting.':'Enter the 6-digit code sent to your email.',
      'Tasdiqlash':'Verify','Kodni qayta yuborish':'Resend code','Parolni tiklash':'Reset password',
      'Emailingizga kod yuboramiz.':'We will send a code to your email.','Kod yuborish':'Send code',
      'Kirishga qaytish':'Back to login','Ma’lumotlaringiz faqat sizga tegishli.':'Your data belongs only to you.',
      'SHAXSIY MOLIYA':'PERSONAL FINANCE','Pulingizni':'Manage your money','ongli boshqaring.':'mindfully.',
      'Kirim, chiqim va maqsadlaringizni bitta sokin, tartibli makonda kuzating.':'Track income, expenses, and goals in one calm, organized place.',
      'Har bir so‘m':'Every sum','o‘z o‘rnida':'in its place','Moliyaviy':'Financial','aniqlik':'clarity',
      'Umumiy ko‘rinish':'Overview','Tranzaksiyalar':'Transactions','Hisoblar':'Accounts','Kategoriyalar':'Categories',
      'MENYU':'MENU','Bugungi moliyaviy holatingizga bir nazar.':'Take a look at your finances today.',
      'Kirim va chiqimlaringizni kuzating.':'Track your income and expenses.',
      'Pul saqlanadigan hisoblaringiz.':'Your money accounts.','Tranzaksiyalaringizni tartibga soling.':'Organize your transactions.',
      'Umumiy balans':'Total balance','Jami kirim':'Total income','Jami chiqim':'Total expenses',
      'Yangi tranzaksiya':'New transaction','Tranzaksiya qo‘shish':'Add transaction',
      'Hisob qo‘shish':'Add account','Kategoriya qo‘shish':'Add category','Hisoblaringiz':'Your accounts',
      'Naqd pul, karta va valyuta hisoblari':'Cash, card, and currency accounts',
      'Chiqim kategoriyalari':'Expense categories','Kirim kategoriyalari':'Income categories',
      'Sarflaringizni guruhlang':'Group your expenses','Daromad manbalari':'Income sources',
      'Barcha turlar':'All types','Barcha hisoblar':'All accounts','Kirim':'Income','Chiqim':'Expense',
      'TRANZAKSIYA':'TRANSACTION','HISOB':'ACCOUNT','KATEGORI':'CATEGORY','SANA':'DATE','SUMMA':'AMOUNT',
      'Saqlash':'Save','Bekor qilish':'Cancel','Yopish':'Close','Yangi':'New',
      'Hisob nomi':'Account name','Hisob turi':'Account type','Naqd pul':'Cash','Bank kartasi':'Bank card',
      'Valyuta':'Currency','Kategoriya nomi':'Category name','Kategoriya turi':'Category type',
      'Tranzaksiya turi':'Transaction type','Hisob':'Account','Kategoriya':'Category','Summa':'Amount',
      'Sana':'Date','Izoh':'Note','Masalan, tushlik...':'For example, lunch...',
      'Tahrirlash':'Edit','O‘chirish':'Delete','Yangilash':'Update',
      'Muvaffaqiyatli saqlandi.':'Saved successfully.','Ma’lumot yangilandi.':'Information updated.',
      'Sessiya tugadi. Qayta kiring.':'Session expired. Please log in again.',
      'Email yoki parol noto‘g‘ri.':'Incorrect email or password.','Foydalanuvchi':'User','Chiqish':'Log out',
      'Oldingi':'Previous','Keyingi':'Next','sahifa':'page','Yaratilgan:':'Created:',
      'Hozircha ma’lumot yo‘q':'No data yet','Kategoriya yo‘q.':'No categories.',
      'Hali hisob yaratilmagan.':'No account created yet.','Hisoblar hali yo‘q. Birinchi hisobingizni qo‘shing.':'No accounts yet. Add your first account.',
      'Bu filtrda tranzaksiya topilmadi.':'No transactions match this filter.',
      'Avval hisob yarating, keyin tranzaksiya qo‘shishingiz mumkin.':'Create an account before adding a transaction.',
        'Avval kirim yoki chiqim kategoriyasini yarating.':'Create an income or expense category first.',
        'Kategoriyani tahrirlash':'Edit category','Hisobni tahrirlash':'Edit account',
        'Tranzaksiyani tahrirlash':'Edit transaction','O‘zgarishlarni saqlash':'Save changes'
    }
  };
  let current = 'uz';
  const originalText = new WeakMap();
  const originalAttrs = new WeakMap();
  const normalize = value => String(value ?? '').replace(/\s+/g, ' ').trim();

  function translateText(value) {
    const dictionary = dictionaries[current] || {};
    const key = normalize(value);
    return dictionary[key] || value;
  }

  function applyTranslations(root = document.body) {
    if (!root) return;
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    const nodes = [];
    while (walker.nextNode()) {
      const node = walker.currentNode;
      if (!originalText.has(node)) originalText.set(node, node.nodeValue);
      nodes.push(node);
    }
    nodes.forEach(node => {
      const source = originalText.get(node);
      const translated = current === 'uz' ? source : translateText(source);
      if (node.nodeValue !== translated) node.nodeValue = translated;
    });

    root.querySelectorAll?.('[placeholder],[title],[aria-label]').forEach(element => {
      ['placeholder', 'title', 'aria-label'].forEach(attribute => {
        if (!element.hasAttribute(attribute)) return;
        let saved = originalAttrs.get(element);
        if (!saved) { saved = {}; originalAttrs.set(element, saved); }
        if (!(attribute in saved)) saved[attribute] = element.getAttribute(attribute);
        const source = saved[attribute];
        const translated = current === 'uz' ? source : translateText(source);
        if (element.getAttribute(attribute) !== translated) element.setAttribute(attribute, translated);
      });
    });
    document.documentElement.lang = current;
  }

  function setLanguage(language) {
    current = Object.prototype.hasOwnProperty.call(dictionaries, language) ? language : 'uz';
    // Sync the selector wherever it is currently rendered.
    ['#authLanguage', '#dashboardLanguage'].forEach(selector => {
      const select = document.querySelector(selector);
      if (select) select.value = current;
    });
    applyTranslations();
    document.dispatchEvent(new CustomEvent('kissa:language', { detail: current }));
  }
  window.KissaI18n = { setLanguage, getLanguage: () => current, applyTranslations, t: translateText };
})();