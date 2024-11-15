let [odd, even] = [[],[]];

function loadCommands(){
  const EVEN = document.querySelector('.even');
  const ODD = document.querySelector('.odd');
  EVEN.innerHTML = "";
  ODD.innerHTML = "";
  let ulEven = document.createElement('ul');
  let ulOdd = document.createElement('ul');
  
  for (const cmd of even){
    ulEven.innerHTML += `<li onclick="select(this)">${cmd}</li>`;
  }
  for (const cmd of odd){
    ulOdd.innerHTML += `<li onclick="select(this)">${cmd}</li>`;
  }
  
  EVEN.appendChild(ulEven)
  ODD.appendChild(ulOdd)
}
window.onload = function(){
  Swal.fire({
    icon: 'info',
    title: 'TELEBOT',
    text: 'Thank you for visiting! We\'re excited to share our site with you.',
    footer: `Made with 🖕, by <a href="https://facebook.com/greegmon.1", target="_blank">Greegmon</a>`
  });
  
  fetch('/getCommands')
    .then(r=>r.json()).then(data => {
      for (let i=0;i<data.length;i++){
        (i % 2) === 0 ? even.push(data[i]):odd.push(data[i])
      }
      loadCommands()
    })
}

function selectAll(){
  const list = document.querySelectorAll("li")
  let btn = document.querySelector('.sa');
  if (btn.classList.contains('selectAll')){
    list.forEach(li => li.classList.contains('selected') ? li.classList.remove('selected'):{})
    btn.classList.remove('selectAll')
    btn.textContent = 'Select All';
  }else{
    list.forEach(li => {
      if (!li.classList.contains('selected')){
        li.classList.add('selected')
      }
    })
    btn.classList.add('selectAll')
    btn.textContent = 'deselect all';
  }
}

function fuck(el){
  const btn = document.querySelector('.addLink');
  const nanay = el.parentElement;
  const [ti,te] = nanay.querySelectorAll('input');
  if (ti.value && te.value){
    if(btn.hasAttribute('disabled')){
      btn.removeAttribute('disabled')
    }
  }else{
    if (!btn.hasAttribute('disabled')){
      btn.setAttribute('disabled', '')
    }
  }
}

function addLink(){
  const links = document.querySelector('.links');
  const [inp1,inp2] = document.querySelectorAll('.links .item:last-child input');
  const item = document.createElement('div')
  item.classList.add('item');
  const input1 = document.createElement('input');
  input1.setAttribute('type', 'text');
  input1.setAttribute('placeholder', 'Label')
  input1.setAttribute('oninput', 'fuck(this)')
  const input2 = document.createElement('input');
  input2.setAttribute('type', 'text');
  input2.setAttribute('placeholder', 'link');
  input2.setAttribute('oninput', 'fuck(this)')
  
  document.querySelector('.addLink').setAttribute('disabled','')
  item.appendChild(input1);
  item.appendChild(input2);
  links.appendChild(item)
}

function isTokenValid(token){
  const j = token.split(':');
  if (token.includes(' ')){
    return ['error', 'Token should not include spaces']
  }else if (j.length !== 2){
    return ['error', 'Invalid bot token']
  }else if (!j[1] || !j[0]){
    return ['error', 'Invalid bot token']
  }else{
    return ['success', null]
  }
}

function active_bots(){
  fetch('/actives').then(r=>r.json()).then(data=>{
    text = '';
    for (const bot of data){
      text += `
        <div class='bot'>
          <div class="thumbnail">
            <img src="${bot.profile}" width='43' alt="${bot.name}">
          </div>
          <div class="info">
            <p class='bot-name'>${bot.name} <span class='bot-id'>${bot.id}</span></p>
            <a class="bot-link" href="https://t.me/${bot.name}" target="_blank">t.me/${bot.name} <i class="fa-solid fa-link"></i></a>
          </div>
        </div>
      `;
    }
    document.querySelector('.active').innerHTML = text
    return
  }).catch(err=>console.error(err))
}

async function login(obj){
  const Toast = Swal.mixin({toast: true,position: "top",showConfirmButton: false,timer: 2300,timerProgressBar: true});
  Toast.fire({
    icon: "info",
    title: "Processing you request."
  });
  try{
    const response = await fetch('/login',{
      method: 'POST',
      headers: {"Content-Type": 'application/json'},
      body: JSON.stringify(obj)
    });
    if (!response.ok){
      const errorData = await response.json();
      Toast.fire({
        icon: 'error',
        title: errorData.message
      })
      throw new Error(errorData.message)
    }
    const data = await response.json();
    Toast.fire({icon:'success',title:'Successfully logged in'})
    document.getElementById('token').value = '';
    document.getElementById('name').value = '';
    document.getElementById('id').value = '';
    loadCommands()
    if(document.querySelector('.sa').classList.contains('selectAll')) document.querySelector('.sa').classList.remove('selectAll')
    document.querySelector('.links').innerHTML = `<div class="item"><input type="text" placeholder="label" oninput="fuck(this)"><input type="text" placeholder="https://example.com/test" oninput="fuck(this)"></div>`;
    active_bots()
  }catch(e){
    Toast.fire({
      icon: 'error',
      title: e.message
    })
    console.error("Error: ",e)
  }
}

function submit(){
  let TOKEN = document.getElementById('token').value.trim();
  let COMMANDS = [];
  let OWNER_NAME = document.getElementById('name').value.trim();
  let OWNER_ID = document.getElementById('id').value.trim();
  let LINKS = [];
  
  const items = document.querySelectorAll('.links .item');
  items.forEach(item => {
    let [inputA, inputB] = item.querySelectorAll('input');
    if (inputA.value && inputB.value){
      LINKS.push([inputA.value,inputB.value])
    }
  })
  const li = document.querySelectorAll("ul .selected");
  for(const h of li){
    COMMANDS.push(h.innerText);
  }
  
  const [status, message] = isTokenValid(TOKEN);
  if(status === 'error'){
    Swal.fire({
      icon: 'error',
      title: status,
      text: message
    })
  }else{
    let yuh = {token: TOKEN,commands: COMMANDS,owner_name: OWNER_NAME,owner_id: OWNER_ID,owner_links: LINKS}
    login(yuh)
  }
}

active_bots()

const select = (li) => {
  li.classList.toggle('selected')
}