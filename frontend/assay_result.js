import {h,empty,badge} from './base.js';
import {stats} from './readout.js';
export function assayResult(rows,canSign){
  if(!rows.length) return empty('纳入至少六对试条后发起置换。');
  const a=rows[0];
  return '<section class="band"><header><h2>同底片精确配对</h2>'+badge(a.eligible?'满足限值':'需要补测')+'</header>'+stats([['样本',a.n+' 对'],['中位增益',a.gain.toFixed(3)],['双侧 p',a.p.toFixed(5)],['最大掉色',a.fade.toFixed(2)]])+'<p>样本指纹 '+h(a.sample_key.slice(0,16))+'</p>'+(a.eligible&&canSign?'<button data-sign="'+a.id+'">签发洗次</button>':'')+'</section>';
}
