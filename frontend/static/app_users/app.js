(() => {
  'use strict';
  const API = '';
  const $ = (selector) => document.querySelector(selector);
  const preferredLanguage = localStorage.getItem('kissa_language') || 'uz';
  if (window.KissaI18n) window.KissaI18n.setLanguage(preferredLanguage);
  const applyLanguage = (lang) => {
    const safe = ['uz','ru','en'].includes(lang) ? lang : 'uz';
    localStorage.setItem('kissa_language', safe);
    document.documentElement.lang = safe;
    ['#authLanguage','#dashboardLanguage','#registerForm [name=language]'].forEach(sel => { const el=$(sel); if(el) el.value=safe; });
    if(window.KissaI18n) window.KissaI18n.setLanguage(safe);
    document.dispatchEvent(new CustomEvent('kissa:language'));
  };
  const state = { access: localStorage.getItem('kissa_access'), refresh: localStorage.getItem('kissa_refresh'), user: null, accounts: [], categories: [], transactions: [], page: 1, next: null, previous: null, currentView: 'overview', editing: null };
  const money = (value, currency='UZS') => `${new Intl.NumberFormat('uz-UZ',{maximumFractionDigits:2}).format(Number(value||0))} <small>${escapeHtml(currency)}</small>`;
  const dateText = (value) => { if(!value) return '—'; const d=new Date(`${value}T00:00:00`); return Number.isNaN(d.getTime()) ? value : d.toLocaleDateString('uz-UZ',{day:'2-digit',month:'short',year:'numeric'}); };
  const escapeHtml = (value) => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const showToast = (message, type='success') => { const el=$('#toast'); if(!el){ window.alert(message); return; } el.textContent=message; el.className=`toast show ${type}`; window.clearTimeout(showToast.timer); showToast.timer=window.setTimeout(()=>el.className='toast global-toast',4500); };
  const showLoginError = (message) => {
    const form = $('#loginForm');
    let error = $('#loginError');

    if (!error) {
        error = document.createElement('div');
        error.id = 'loginError';
        error.className = 'login-error';

        const button = form.querySelector('button[type="submit"]');

        if (button) {
            form.insertBefore(error, button);
        } else {
            form.appendChild(error);
        }
    }

    error.textContent = message;
    error.classList.add('show');
};

const clearLoginError = () => {
    const error = $('#loginError');
    if (error) {
        error.classList.remove('show');
    }
};
  const responseMessage = (data) => { if(!data) return 'Xatolik yuz berdi'; if(typeof data==='string') return data; if(data.message) return data.message; const values=Object.values(data); const first=values[0]; if(Array.isArray(first)) return String(first[0] ?? 'So‘rov bajarilmadi'); if(typeof first==='string') return first; if(first && typeof first==='object') return responseMessage(first); return 'So‘rov bajarilmadi'; };
  async function request(path, options={}) {
    const headers = {'Content-Type':'application/json', ...(options.headers||{})};
    if(state.access && !options.noAuth) headers.Authorization=`Bearer ${state.access}`;
    let response=await fetch(`${API}${path}`,{...options,headers});
    if(response.status===401 && state.refresh && !options.noAuth && !options.retried){
      try { const refreshResponse=await fetch('/token/refresh/',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({refresh:state.refresh})}); const tokens=await refreshResponse.json(); if(refreshResponse.ok&&tokens.access){saveTokens(tokens); return request(path,{...options,retried:true});} } catch(_e){}
      clearSession(); showAuth('login'); throw new Error('Sessiya tugadi. Qayta kiring.');
    }
    let data=null; if(response.status!==204){const text=await response.text(); try{data=text?JSON.parse(text):null}catch(_e){data={message:text||response.statusText}}}
    if(!response.ok) throw new Error(responseMessage(data)||`HTTP ${response.status}`);
    return data;
  }
  const saveTokens=(tokens)=>{state.access=tokens.access;state.refresh=tokens.refresh;localStorage.setItem('kissa_access',tokens.access);localStorage.setItem('kissa_refresh',tokens.refresh);};
  const clearSession=()=>{state.access=state.refresh=null;localStorage.removeItem('kissa_access');localStorage.removeItem('kissa_refresh');};
  const showAuth=(mode='login')=>{$('#authShell').classList.remove('hidden');$('#appShell').classList.add('hidden');setAuthTab(mode);};
  const setAuthTab=(mode)=>{document.querySelectorAll('[data-auth-tab]').forEach(b=>b.classList.toggle('active',b.dataset.authTab===mode));['login','register','otp','reset'].forEach(k=>{const el=$(`#${k}Form`);if(el)el.classList.toggle('hidden',k!==mode)});};
  const showApp=()=>{$('#authShell').classList.add('hidden');$('#appShell').classList.remove('hidden');};
  const bindAuth=()=>{
    document.querySelectorAll('[data-auth-tab]').forEach(b=>b.addEventListener('click',()=>setAuthTab(b.dataset.authTab)));
    ['#authLanguage','#dashboardLanguage','#registerForm [name=language]'].forEach(sel=>{const el=$(sel);if(el)el.addEventListener('change',()=>applyLanguage(el.value));});
    applyLanguage(preferredLanguage);
    $('#loginForm').querySelectorAll('input').forEach(input=>input.addEventListener('input',clearLoginError));
    $('#loginForm').addEventListener('submit',async e=>{e.preventDefault();clearLoginError();const f=new FormData(e.currentTarget);try{const data=await request('/login/',{method:'POST',noAuth:true,body:JSON.stringify({email:f.get('email'),password:f.get('password')})});saveTokens(data.tokens);await initApp();}catch(err){showLoginError(err.message)}});
    $('#registerForm').addEventListener('submit',async e=>{e.preventDefault();const f=new FormData(e.currentTarget);const body=Object.fromEntries(f.entries());const chosenLanguage=localStorage.getItem('kissa_language')||$('#authLanguage').value||body.language||'uz';body.language=chosenLanguage;applyLanguage(chosenLanguage);try{await request('/register/',{method:'POST',noAuth:true,body:JSON.stringify(body)});$('#otpForm [name=email]').value=body.email;setAuthTab('otp');showToast('Tasdiqlash kodi emailingizga yuborildi.');}catch(err){showToast(err.message,'error')}});
    $('#otpForm').addEventListener('submit',async e=>{e.preventDefault();const f=new FormData(e.currentTarget);try{const data=await request('/verify-otp/',{method:'POST',noAuth:true,body:JSON.stringify(Object.fromEntries(f.entries()))});saveTokens(data.tokens);await initApp();}catch(err){showToast(err.message,'error')}});
    $('#resendOtp').addEventListener('click',async()=>{try{await request('/resend-otp/',{method:'POST',noAuth:true,body:JSON.stringify({email:$('#otpForm [name=email]').value})});showToast('Yangi kod yuborildi.');}catch(err){showToast(err.message,'error')}});
    $('#forgotBtn').addEventListener('click',()=>setAuthTab('reset'));$('#backLogin').addEventListener('click',()=>setAuthTab('login'));
    $('#resetForm').addEventListener('submit',async e=>{e.preventDefault();const f=new FormData(e.currentTarget);try{await request('/password-reset/request/',{method:'POST',noAuth:true,body:JSON.stringify({email:f.get('email')})});showToast('Emailga tiklash kodi yuborildi. Keyingi bosqich API orqali bajariladi.');}catch(err){showToast(err.message,'error')}});
  };
  const setView=(view)=>{state.currentView=view;const titles={overview:'Umumiy ko‘rinish',transactions:'Tranzaksiyalar',accounts:'Hisoblar',categories:'Kategoriyalar'};document.querySelectorAll('.view-section').forEach(el=>el.classList.add('hidden'));$(`#${view}View`).classList.remove('hidden');document.querySelectorAll('[data-view]').forEach(el=>el.classList.toggle('active',el.dataset.view===view));$('#crumbTitle').textContent=titles[view];$('#pageTitle').innerHTML=`${titles[view]}<span class="title-dot">.</span>`;$('#pageSubtitle').textContent=({overview:'Bugungi moliyaviy holatingizga bir nazar.',transactions:'Kirim va chiqimlaringizni kuzating.',accounts:'Pul saqlanadigan hisoblaringiz.',categories:'Tranzaksiyalaringizni tartibga soling.'})[view];$('#sidebar').classList.remove('open');if(view==='transactions')loadTransactions(1);};
  async function loadData(){const [accounts,categories,transactions,user]=await Promise.all([request('/accounts/'),request('/categories/'),request('/transactions/?page_size=100'),request('/profile/')]);state.accounts=accounts;state.categories=categories;state.transactions=Array.isArray(transactions)?transactions:(transactions.results||[]);state.user=user;renderAll();}
  async function initApp(){try{await loadData();const lang=localStorage.getItem('kissa_language')||state.user?.language||'uz';applyLanguage(lang);showApp();$('#userName').textContent=state.user.first_name||state.user.username||state.user.email;const initial=(state.user.first_name||state.user.username||'K').slice(0,1).toUpperCase();$('#userAvatar').textContent=initial;$('#topAvatar').textContent=initial;$('#todayText').textContent=new Date().toLocaleDateString('uz-UZ',{weekday:'short',day:'numeric',month:'short'});setView(state.currentView||'overview');}catch(err){clearSession();showAuth('login');showToast(err.message,'error')}}
  function renderAll(){renderMetrics();renderAccountPreview();renderRecent();renderAccountGrid();renderCategories();fillAccountFilter();}
  function renderMetrics(){const total=state.accounts.reduce((sum,a)=>sum+Number(a.balance||0),0);const income=state.transactions.filter(t=>t.type==='income').reduce((sum,t)=>sum+Number(t.amount||0),0);const expense=state.transactions.filter(t=>t.type==='expense').reduce((sum,t)=>sum+Number(t.amount||0),0);$('#totalBalance').innerHTML=money(total);$('#totalIncome').innerHTML=money(income);$('#totalExpense').innerHTML=money(expense);const max=Math.max(income,expense,1);$('#flowChart').innerHTML=`<div class="bar-group"><div class="bar-pair"><div class="bar income-bar" style="height:${Math.max(income/max*100,2)}%" title="Kirim"></div><div class="bar expense-bar" style="height:${Math.max(expense/max*100,2)}%" title="Chiqim"></div></div><span class="bar-label">Jami</span></div>`;$('#flowInsight').textContent=income||expense?`Sof oqim: ${new Intl.NumberFormat('uz-UZ',{maximumFractionDigits:0}).format(income-expense)} UZS`:'Hozircha ma’lumot yo‘q';}
  const accountIcon=(type)=>({cash:'◉',card:'▣',currency:'◇'})[type]||'◉';
  function renderAccountPreview(){const target=$('#accountPreview');if(!state.accounts.length){target.innerHTML='<div class="empty-state">Hisoblar hali yo‘q. Birinchi hisobingizni qo‘shing.</div>';return;}target.innerHTML=state.accounts.slice(0,4).map(a=>`<div class="account-row"><div class="account-icon">${accountIcon(a.type)}</div><div class="account-info"><b>${escapeHtml(a.name)}</b><small>${escapeHtml(a.type)} · ${escapeHtml(a.currency)}</small></div><div class="account-amount">${money(a.balance,a.currency)}</div></div>`).join('');}
  function transactionRow(t,withAccount=true){const type=t.type==='income'?'income':'expense';return `<tr><td><div class="transaction-name"><span class="transaction-symbol ${type}">${type==='income'?'↙':'↗'}</span><span>${escapeHtml(t.description||t.category_name||'Tranzaksiya')}</span></div></td>${withAccount?`<td>${escapeHtml(t.account_name||accountById(t.account)?.name||'—')}</td>`:''}<td>${escapeHtml(t.category_name||categoryById(t.category)?.name||'—')}</td><td>${dateText(t.date)}</td><td class="align-right ${type==='income'?'amount-income':'amount-expense'}">${type==='income'?'+':'−'}${new Intl.NumberFormat('uz-UZ',{maximumFractionDigits:2}).format(Number(t.amount||0))} ${escapeHtml(accountById(t.account)?.currency||'UZS')}</td><td><div class="row-actions"><button class="row-action" title="Tahrirlash" data-edit-transaction="${t.id}">✎</button><button class="row-action" title="O‘chirish" data-delete-transaction="${t.id}">×</button></div></td></tr>`;}
  const accountById=id=>state.accounts.find(a=>a.id===Number(id));const categoryById=id=>state.categories.find(c=>c.id===Number(id));
  function renderRecent(){const rows=$('#recentRows');if(!state.transactions.length){rows.innerHTML='<tr><td colspan="5" class="empty-cell">Hozircha tranzaksiya yo‘q. Birinchi tranzaksiyani qo‘shing.</td></tr>';return;}rows.innerHTML=state.transactions.slice(0,5).map(t=>transactionRow(t,false)).join('');}
  function renderAccountGrid(){const target=$('#accountGrid');if(!state.accounts.length){target.innerHTML='<div class="panel empty-state">Hali hisob yaratilmagan.</div>';return;}target.innerHTML=state.accounts.map(a=>`<article class="account-card"><div class="account-icon">${accountIcon(a.type)}</div><div class="account-info"><b>${escapeHtml(a.name)}</b><small>${escapeHtml(a.type)} · ${escapeHtml(a.currency)}</small></div><div class="account-amount">${money(a.balance,a.currency)}</div><div class="account-type">Yaratilgan: ${dateText(a.created_at?.slice(0,10))}</div><div class="row-actions"><button class="row-action" data-edit-account="${a.id}" title="Tahrirlash">✎</button><button class="row-action" data-delete-account="${a.id}" title="O‘chirish">×</button></div></article>`).join('');}
  function renderCategories(){for(const type of ['expense','income']){const el=type==='expense'?$('#expenseCategories'):$('#incomeCategories');const list=state.categories.filter(c=>c.type===type);el.innerHTML=list.length?list.map(c=>`<div class="category-item"><div class="category-bullet">${type==='expense'?'↗':'↙'}</div><div class="account-info"><b>${escapeHtml(c.name)}</b><small>${type==='expense'?'Chiqim':'Kirim'} kategoriyasi</small></div><div class="row-actions"><button class="row-action" data-edit-category="${c.id}" title="Tahrirlash">✎</button><button class="row-action" data-delete-category="${c.id}" title="O‘chirish">×</button></div></div>`).join(''):'<div class="empty-state">Kategoriya yo‘q.</div>';}}
  function fillAccountFilter(){const select=$('#transactionAccountFilter');const current=select.value;select.innerHTML='<option value="">Barcha hisoblar</option>'+state.accounts.map(a=>`<option value="${a.id}">${escapeHtml(a.name)}</option>`).join('');select.value=current;}
  async function loadTransactions(page=1){state.page=page;const params=new URLSearchParams({page:String(page),page_size:'10'});const type=$('#transactionTypeFilter').value,account=$('#transactionAccountFilter').value;if(type)params.set('type',type);if(account)params.set('account',account);try{const data=await request(`/transactions/?${params}`);const rows=Array.isArray(data)?data:(data.results||[]);state.next=data.next;state.previous=data.previous;$('#transactionRows').innerHTML=rows.length?rows.map(t=>transactionRow(t,true)).join(''):'<tr><td colspan="6" class="empty-cell">Bu filtrda tranzaksiya topilmadi.</td></tr>';$('#pagination').innerHTML=`<button id="prevPage" ${!state.previous?'disabled':''}>← Oldingi</button><span style="align-self:center;font-size:11px;color:#8b96a7">${page}-sahifa</span><button id="nextPage" ${!state.next?'disabled':''}>Keyingi →</button>`;$('#prevPage').addEventListener('click',()=>loadTransactions(Math.max(1,page-1)));$('#nextPage').addEventListener('click',()=>loadTransactions(page+1));}catch(err){showToast(err.message,'error')}}
  const field=(label,name,type='text',value='',extra='')=>`<label class="field-label">${label}<input class="field-control" name="${name}" type="${type}" value="${escapeHtml(value)}" ${extra}></label>`;
  const selectField=(label,name,options,value='')=>`<label class="field-label">${label}<select class="field-control" name="${name}" required>${options.map(o=>`<option value="${o.value}" ${String(o.value)===String(value)?'selected':''}>${escapeHtml(o.label)}</option>`).join('')}</select></label>`;
  function openModal(title,fields,submitLabel='Saqlash',editing=null){state.editing=editing;$('#modalTitle').textContent=title;$('#modalFields').innerHTML=fields;$('#modalSubmit').innerHTML=`${submitLabel} <span>↗</span>`;$('#modalBackdrop').classList.remove('hidden');}
  const closeModal=()=>{$('#modalBackdrop').classList.add('hidden');$('#modalForm').reset();state.editing=null;};
  function accountForm(account=null){openModal(account?'Hisobni tahrirlash':'Yangi hisob',field('Hisob nomi','name','text',account?.name||'','required')+selectField('Hisob turi','type',[{value:'cash',label:'Naqd pul'},{value:'card',label:'Bank kartasi'},{value:'currency',label:'Valyuta'}],account?.type||'cash')+field('Valyuta','currency','text',account?.currency||'UZS','required maxlength="10"'),account?'Yangilash':'Hisob yaratish',{kind:'account',id:account?.id});}
  function categoryForm(category=null){openModal(category?'Kategoriyani tahrirlash':'Yangi kategoriya',field('Kategoriya nomi','name','text',category?.name||'','required')+selectField('Kategoriya turi','type',[{value:'expense',label:'Chiqim'},{value:'income',label:'Kirim'}],category?.type||'expense'),category?'Yangilash':'Kategoriya yaratish',{kind:'category',id:category?.id});}
  function transactionForm(t=null){if(!state.accounts.length){showToast('Avval hisob yarating, keyin tranzaksiya qo‘shishingiz mumkin.','error');accountForm();return;}if(!state.categories.length){showToast('Avval kirim yoki chiqim kategoriyasini yarating.','error');categoryForm();return;}const accOpts=state.accounts.map(a=>({value:a.id,label:`${a.name} (${a.currency})`}));const catOpts=(type)=>state.categories.filter(c=>c.type===type).map(c=>({value:c.id,label:c.name}));const type=t?.type||'expense';const fields=selectField('Tranzaksiya turi','type',[{value:'expense',label:'Chiqim'},{value:'income',label:'Kirim'}],type)+selectField('Hisob','account',accOpts,t?.account||state.accounts[0]?.id)+`<div id="transactionCategoryField">${selectField('Kategoriya','category',catOpts(type),t?.category||state.categories.find(c=>c.type===type)?.id)}</div>`+field('Summa','amount','number',t?.amount||'','required min="0.01" step="0.01"')+field('Sana','date','date',t?.date||new Date().toISOString().slice(0,10),'required')+`<label class="field-label">Izoh<textarea class="field-control" style="height:85px;padding:12px;resize:vertical" name="description" placeholder="Masalan, tushlik...">${escapeHtml(t?.description||'')}</textarea></label>`;openModal(t?'Tranzaksiyani tahrirlash':'Yangi tranzaksiya',fields,t?'O‘zgarishlarni saqlash':'Tranzaksiya qo‘shish',{kind:'transaction',id:t?.id});$('#modalFields [name=type]').addEventListener('change',e=>{$('#transactionCategoryField').innerHTML=selectField('Kategoriya','category',catOpts(e.target.value),state.categories.find(c=>c.type===e.target.value)?.id);});}
  async function submitModal(e){e.preventDefault();const f=new FormData(e.currentTarget);const body=Object.fromEntries(f.entries());const edit=state.editing;try{if(edit?.kind==='account'){await request(edit.id?`/accounts/${edit.id}/update/`:'/accounts/create/',{method:edit.id?'PUT':'POST',body:JSON.stringify(body)});}else if(edit?.kind==='category'){await request(edit.id?`/categories/${edit.id}/update/`:'/categories/create/',{method:edit.id?'PUT':'POST',body:JSON.stringify(body)});}else if(edit?.kind==='transaction'){body.amount=Number(body.amount);body.account=Number(body.account);body.category=Number(body.category);await request(edit.id?`/transactions/${edit.id}/update/`:'/transactions/create/',{method:edit.id?'PATCH':'POST',body:JSON.stringify(body)});}closeModal();await loadData();if(state.currentView==='transactions')await loadTransactions(state.page);showToast(edit?.id?'Ma’lumot yangilandi.':'Muvaffaqiyatli saqlandi.');}catch(err){showToast(err.message,'error')}}
  async function deleteResource(path,label){if(!window.confirm(`${label}ni o‘chirishni tasdiqlaysizmi?`))return;try{await request(path,{method:'DELETE'});await loadData();if(state.currentView==='transactions')await loadTransactions(state.page);showToast(`${label} o‘chirildi.`);}catch(err){showToast(err.message,'error')}}
  function bindApp(){document.querySelectorAll('[data-view]').forEach(b=>b.addEventListener('click',()=>setView(b.dataset.view)));$('#logoutBtn').addEventListener('click',()=>{clearSession();showAuth('login')});$('#refreshBtn').addEventListener('click',()=>initApp());$('#newTransactionBtn').addEventListener('click',()=>transactionForm());$('#transactionCreateBtn').addEventListener('click',()=>transactionForm());$('#accountCreateBtn').addEventListener('click',()=>accountForm());$('#addAccountBtn').addEventListener('click',()=>accountForm());$('#categoryCreateBtn').addEventListener('click',()=>categoryForm());$('#transactionTypeFilter').addEventListener('change',()=>loadTransactions(1));$('#transactionAccountFilter').addEventListener('change',()=>loadTransactions(1));$('#modalClose').addEventListener('click',closeModal);$('#modalCancel').addEventListener('click',closeModal);$('#modalBackdrop').addEventListener('click',e=>{if(e.target===$('#modalBackdrop'))closeModal()});$('#modalForm').addEventListener('submit',submitModal);$('#mobileMenu').addEventListener('click',()=>$('#sidebar').classList.toggle('open'));
    document.addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;const id=b.dataset.editAccount;if(id)accountForm(state.accounts.find(a=>a.id===Number(id)));if(b.dataset.deleteAccount)deleteResource(`/accounts/${b.dataset.deleteAccount}/delete/`,'Hisob');if(b.dataset.editCategory)categoryForm(state.categories.find(c=>c.id===Number(b.dataset.editCategory)));if(b.dataset.deleteCategory)deleteResource(`/categories/${b.dataset.deleteCategory}/delete/`,'Kategoriya');if(b.dataset.editTransaction){const t=state.transactions.find(t=>t.id===Number(b.dataset.editTransaction));if(t)transactionForm(t);else request(`/transactions/${b.dataset.editTransaction}/`).then(transactionForm).catch(err=>showToast(err.message,'error'));}if(b.dataset.deleteTransaction)deleteResource(`/transactions/${b.dataset.deleteTransaction}/delete/`,'Tranzaksiya');});}
  if (window.KissaI18n) {
    const observer = new MutationObserver(() => {
      // applyTranslations writes only changed values, so this observer settles
      // instead of endlessly observing its own identical text assignments.
      window.KissaI18n.applyTranslations();
    });
    observer.observe(document.body, {childList:true,subtree:true,characterData:true});
    document.addEventListener('kissa:language', () => window.KissaI18n.applyTranslations());
  }
  bindAuth();bindApp();if(state.access)initApp();else showAuth('login');
})();