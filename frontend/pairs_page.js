import {notice} from './base.js';
import {intro} from './readout.js';
import {onSubmit,feedback} from './submit.js';
import {cyan,plate} from './cyan_api.js';
import {stripRows,controls,conflicts} from './strips_view.js';
import {form,bind,reading} from './strip_form.js';
export async function render(outlet,user,message=''){
  const rows=await cyan(plate+'/strips');
  const [edition]=await cyan('/plates');
  const editable=edition.state==='open';
  outlet.innerHTML=intro('试条配对与隔离','短洗和长洗各报一侧；缺一侧先等补齐，同侧多份读数两份都留并隔离。')+
    '<div class="stripdesk"><div>'+stripRows(rows)+'</div><aside class="entry">'+
    (editable&&user.role==='reviewer'?controls(rows):'')+
    (editable&&user.role==='reviewer'?conflicts(rows):'')+
    feedback+(editable&&user.role==='operator'?form():'')+'</aside></div>';
  const status=outlet.querySelector('.stripdesk aside > [role=status]');
  if(message) notice(status,message);
  const entry=outlet.querySelector('aside form[data-reading]');
  bind(entry);
  onSubmit(entry,async data=>{await cyan(plate+'/strips','POST',reading(data));await render(outlet,user,'读数已上报');});
  for(const btn of outlet.querySelectorAll('[data-include]')) btn.onclick=async()=>{
    try {await cyan(plate+'/strips/'+encodeURIComponent(btn.dataset.code)+'/qualify?include='+btn.dataset.include,'POST');await render(outlet,user,'已登记复核结果');}
    catch(err){notice(status,err.message,true);}
  };
  for(const panel of outlet.querySelectorAll('[data-conflict]')) onSubmit(panel,async data=>{
    const body={};
    for(const side of ['short','long']) if(data[side]) body[side]=Number(data[side]);
    await cyan(plate+'/strips/'+encodeURIComponent(panel.dataset.conflict)+'/select','POST',body);
    await render(outlet,user,'已选定读数，待温差复核');
  });
}
