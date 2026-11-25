import {notice} from './base.js';
import {intro} from './readout.js';
import {onSubmit,feedback} from './submit.js';
import {cyan,plate} from './cyan_api.js';
import {stripRows,controls} from './strips_view.js';
import {form,reading} from './strip_form.js';
export async function render(outlet,user,message=''){
  const rows=await cyan(plate+'/strips');
  const [edition]=await cyan('/plates');
  const editable=edition.state==='open';
  outlet.innerHTML=intro('试条配对与隔离','温差超 2°C 的配对单独隔离，保留原始测量。')+'<div class="stripdesk"><div>'+stripRows(rows)+'</div><aside class="entry">'+(editable&&user.role==='reviewer'?controls(rows):'')+feedback+(editable&&user.role==='operator'?form():'')+'</aside></div>';
  const status=outlet.querySelector('[role=status]');
  if(message) notice(status,message);
  onSubmit(outlet.querySelector('form'),async data=>{await cyan(plate+'/strips','POST',reading(data));await render(outlet,user,'试条已登记');});
  for(const btn of outlet.querySelectorAll('[data-code]')) btn.onclick=async()=>{
    try {await cyan(plate+'/strips/'+encodeURIComponent(btn.dataset.code)+'/qualify?include='+btn.dataset.include,'POST');await render(outlet,user,'已登记复核结果');}
    catch(err){notice(status,err.message,true);}
  };
}
