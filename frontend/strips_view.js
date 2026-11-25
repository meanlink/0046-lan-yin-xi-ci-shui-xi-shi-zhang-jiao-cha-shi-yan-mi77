import {h,badge} from './base.js';
import {table} from './readout.js';
export const states={pending:'待复核',paired:'纳入',excluded:'隔离'};
export function stripRows(rows){
  return table('试条密度配对',['试条','短洗温度','长洗温度','短洗密度','长洗密度','掉色','证据状态'],
    rows.map(x=>[x.code,x.short_temp+' °C',x.long_temp+' °C',x.short_density,x.long_density,x.long_fade,states[x.state]]));
}
export function controls(rows){
  return rows.filter(x=>x.state==='pending').map(x=>'<div><b>'+h(x.code)+'</b> '+badge(states[x.state])+' <button data-code="'+h(x.code)+'" data-include="true">纳入</button> <button class="quiet" data-code="'+h(x.code)+'" data-include="false">隔离</button></div>').join('');
}
