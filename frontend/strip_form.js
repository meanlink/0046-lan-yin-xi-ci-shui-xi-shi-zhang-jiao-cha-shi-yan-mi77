import {feedback} from './submit.js';
const sideNames={short:'短洗',long:'长洗'};
export function form(){
  return '<form class="entry" data-reading><h2>登记单侧读数</h2><label>试条编号 <input name="code" required pattern="[A-Z0-9-]{2,20}"></label>'+
    '<label>仪器侧别 <select name="side" data-side>'+Object.entries(sideNames).map(([k,v])=>'<option value="'+k+'">'+v+'</option>').join('')+'</select></label>'+
    '<label>水温 °C <input type="number" name="temp" min="4" max="70" step=".01" required></label>'+
    '<label>密度 <input type="number" name="density" min="0" max="2" step=".01" required></label>'+
    '<label data-fade>长洗掉色 <input type="number" name="fade" min="0" max="1" step=".01"></label>'+
    '<button>上报读数</button>'+feedback+'</form>';
}
export function bind(form){
  if(!form) return;
  const side=form.querySelector('[data-side]');
  const fade=form.querySelector('[data-fade]');
  const sync=()=>{
    fade.hidden=side.value!=='long';
    fade.querySelector('input').required=side.value==='long';
  };
  side.onchange=sync;
  sync();
}
export function reading(data){
  const out={code:data.code,side:data.side,temp:Number(data.temp),density:Number(data.density)};
  if(data.side==='long') out.fade=Number(data.fade);
  return out;
}
