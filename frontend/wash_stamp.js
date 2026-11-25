const schedule=new Intl.DateTimeFormat('zh-CN',{dateStyle:'medium',timeStyle:'short',timeZone:'Asia/Shanghai'});
export const printTime=value=>schedule.format(new Date(value));
