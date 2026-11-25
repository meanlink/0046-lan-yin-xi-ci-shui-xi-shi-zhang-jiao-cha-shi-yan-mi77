import {feedback} from './submit.js';
const values={short_temp:'短洗水温',long_temp:'长洗水温',short_density:'短洗密度',long_density:'长洗密度',long_fade:'长洗掉色'};
export function form(){
  return '<form class="entry"><h2>添加试条</h2><label>试条编号 <input name="code" required></label>'+Object.entries(values).map(([k,v])=>'<label>'+v+' <input type="number" name="'+k+'" min="0" step=".01" required></label>').join('')+'<button>保存待复核</button>'+feedback+'</form>';
}
export function reading(data){
  for(const key of Object.keys(values)) data[key]=Number(data[key]);
  return data;
}
