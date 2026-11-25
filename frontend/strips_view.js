import {h,badge} from './base.js';
import {table} from './readout.js';
import {feedback} from './submit.js';
export const states={incomplete:'待补齐',pending:'待复核',paired:'纳入',excluded:'隔离'};
const sideNames={short:'短洗',long:'长洗'};

function show(reading,count){
  if(!count) return '—';
  if(count>1) return count+' 份读数待选定';
  return reading.temp+' °C / '+reading.density+(reading.fade==null?'':' / 掉色 '+reading.fade);
}
function status(x){
  if(x.conflict) return '冲突隔离';
  return states[x.state]??x.state;
}
export function stripRows(rows){
  return table('试条密度配对',['试条','短洗','长洗','温差','证据状态'],
    rows.map(x=>[x.code,show(x.short,x.short_active),show(x.long,x.long_active),
      x.temp_gap==null?'—':x.temp_gap+' °C',status(x)]));
}
export function controls(rows){
  return rows.filter(x=>x.state==='pending'&&!x.conflict).map(x=>'<div><b>'+h(x.code)+'</b> '+badge(states[x.state])+' <button data-code="'+h(x.code)+'" data-include="true">纳入</button> <button class="quiet" data-code="'+h(x.code)+'" data-include="false">隔离</button></div>').join('');
}
export function conflicts(rows){
  return rows.filter(x=>x.conflict).map(x=>{
    const picks=['short','long'].filter(side=>x[side+'_active']>1).map(side=>{
      const options=x[side+'_readings'].filter(r=>r.state==='active')
        .map(r=>'<option value="'+r.id+'">'+h(r.temp+' °C / '+r.density+(r.fade==null?'':' / 掉色 '+r.fade))+'</option>').join('');
      return '<label>'+sideNames[side]+'读数 <select name="'+side+'">'+options+'</select></label>';
    }).join('');
    return '<form class="entry" data-conflict="'+h(x.code)+'"><h2>'+h(x.code)+' 同侧多份读数</h2>'+
      '<p class="muted">两份都留档；选定后重新走温差复核。</p>'+picks+
      '<button>确认选定</button>'+feedback+'</form>';
  }).join('');
}
