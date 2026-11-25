import {h,badge,empty} from './base.js';
import {intro} from './readout.js';
import {cyan} from './cyan_api.js';
export async function render(outlet){
  const rows=await cyan('/plates');
  const plate=rows[0];
  outlet.innerHTML=intro('同底片的两种水洗时长','每张试条保留本次对应的水温、密度和试印归属。');
  outlet.innerHTML+=plate?'<div class="contact"><p>'+h(plate.code)+'　'+h(plate.paper)+'</p><h2>'+h(plate.negative)+'</h2><p>'+h(plate.short_sec)+' 秒 / '+h(plate.long_sec)+' 秒</p>'+badge(plate.state==='sealed'?'已定版':'验版中')+'</div><a href="#pairs">查看配对试条</a>':empty('试印版簿为空。');
}
