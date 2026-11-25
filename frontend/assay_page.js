import {waitJob,notice} from './base.js';
import {intro} from './readout.js';
import {feedback} from './submit.js';
import {cyan,plate} from './cyan_api.js';
import {assayResult} from './assay_result.js';
export async function render(outlet,user){
  const rows=await cyan(plate+'/assays');
  const [edition]=await cyan('/plates');
  const allowed=user.role==='reviewer'&&edition.state==='open';
  outlet.innerHTML=intro('水洗效果置换比对','增益用于评估密度提升，掉色用于判断配方是否可签发。')+(allowed?'<button data-run>运行检验</button>':'')+feedback+assayResult(rows,allowed);
  const run=outlet.querySelector('[data-run]'), sign=outlet.querySelector('[data-sign]');
  if(run) run.onclick=async()=>{
    run.disabled=true;
    try{await waitJob((await cyan(plate+'/assays','POST')).job_id); await render(outlet,user);}
    catch(err){notice(outlet.querySelector('[role=status]'),err.message,true);run.disabled=false;}
  };
  if(sign) sign.onclick=async()=>{
    try{await cyan(plate+'/recipe?assay='+sign.dataset.sign,'POST'); location.hash='recipe';}
    catch(err){notice(outlet.querySelector('[role=status]'),err.message,true);}
  };
}
