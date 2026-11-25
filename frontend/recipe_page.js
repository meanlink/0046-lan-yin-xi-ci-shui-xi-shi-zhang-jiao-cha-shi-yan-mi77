import {h,empty} from './base.js';
import {intro} from './readout.js';
import {cyan} from './cyan_api.js';
import {printTime} from './wash_stamp.js';
export async function render(outlet){
  const rows=await cyan('/recipes');
  outlet.innerHTML=intro('定版纸样工签','印刷师按原版纸号执行。同底片两张试条的温差上限为 2°C。')+(rows.map(r=>'<article class="contact"><h2>'+h(r.plate)+' · 水洗 '+r.wash_sec+' 秒</h2><p>证据号 '+r.assay+'</p><p>'+h(r.signer)+' · '+h(printTime(r.signed_at))+'</p></article>').join('')||empty('待复核员从置换比对签入工单。'));
}
