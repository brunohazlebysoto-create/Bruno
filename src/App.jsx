import React, { useState, useEffect, useRef } from "react";
import { Flame, Beef, Wheat, Droplet, Plus, Minus, Trash2, Send, Utensils, MessageSquare, NotebookPen, Loader2, Scale, Camera, Clock, ChefHat, Sparkles, LineChart, Dumbbell, ClipboardList, GlassWater, Target, CalendarDays, ShoppingCart, Activity } from "lucide-react";

/* ===== perfil, presets, split ===== */
const PRESETS = {
  definicion:   { label:"Definición",    kcal:2600, p:220, c:265, f:70 },
  mantenimiento:{ label:"Mantenimiento", kcal:3000, p:200, c:360, f:85 },
  volumen:      { label:"Volumen",       kcal:3400, p:200, c:450, f:90 },
};
// Split de 4 días — B = Pierna Cuádriceps + Hombros (mismo día)
const SPLIT = [
  { key:"A", name:"Pecho + Bíceps", fuel:"Carbo medio", ex:["Press banca","Press inclinado mancuerna","Aperturas","Curl inclinado","Curl martillo","Curl prono barra"] },
  { key:"B", name:"Pierna Cuádriceps + Hombros", fuel:"Carbo alto", ex:["Sentadilla","Prensa 45°","Sentadilla búlgara","Sentadilla ciclista Smith","Extensión cuádriceps","Press Arnold","Vuelos laterales","Vuelos posteriores polea"] },
  { key:"C", name:"Espalda + Tríceps", fuel:"Carbo medio-alto", ex:["Dominadas / Jalón","Remo barra","Remo máquina","Pullover polea","Face pull","Press cerrado","Extensión polea","Extensión sobre cabeza"] },
  { key:"D", name:"Pierna Posterior", fuel:"Carbo alto", ex:["Peso muerto","Leg curl sentado","Puente glúteos","Estocada atrás Smith"] },
];
const MUSCLES = {
  "Press banca":["Pectoral","Tríceps","Deltoide ant."],"Press inclinado mancuerna":["Pectoral superior","Deltoide ant.","Tríceps"],"Aperturas":["Pectoral"],
  "Curl inclinado":["Bíceps (c. larga)"],"Curl martillo":["Braquial","Braquiorradial","Bíceps"],"Curl prono barra":["Braquiorradial","Antebrazo","Bíceps"],
  "Sentadilla":["Cuádriceps","Glúteos","Isquios"],"Prensa 45°":["Cuádriceps","Glúteos"],"Sentadilla búlgara":["Cuádriceps","Glúteos"],"Sentadilla ciclista Smith":["Cuádriceps"],"Extensión cuádriceps":["Cuádriceps"],
  "Press Arnold":["Deltoide ant.","Deltoide lat.","Tríceps"],"Vuelos laterales":["Deltoide lateral"],"Vuelos posteriores polea":["Deltoide posterior"],
  "Dominadas / Jalón":["Dorsal ancho","Bíceps","Romboides"],"Remo barra":["Dorsal ancho","Trapecio medio","Romboides","Bíceps"],"Remo máquina":["Dorsal ancho","Trapecio medio"],"Pullover polea":["Dorsal ancho"],"Face pull":["Deltoide post.","Trapecio","Manguito rotador"],
  "Press cerrado":["Tríceps","Pectoral"],"Extensión polea":["Tríceps"],"Extensión sobre cabeza":["Tríceps (c. larga)"],
  "Peso muerto":["Isquios","Glúteos","Erectores","Espalda"],"Leg curl sentado":["Isquiotibiales"],"Puente glúteos":["Glúteos"],"Estocada atrás Smith":["Glúteos","Cuádriceps","Isquios"],
};
const MEALS = [
  { slot:"Desayuno", kcal:"~580", opts:["4 huevos + 2 claras, 80 g avena con plátano, café","Yogur griego 250 g + 60 g granola + frutos rojos + nueces","Tortilla de 3 huevos + pan integral con aguacate"] },
  { slot:"Almuerzo", kcal:"~620", opts:["180 g pollo, 180 g arroz, verduras, aceite oliva","200 g salmón al horno, 250 g boniato, espárragos","Bowl: 150 g carne magra, quinoa, frijoles, pico de gallo"] },
  { slot:"Pre-entreno", kcal:"~310", opts:["1 plátano + 1 scoop proteína (60-90 min antes)","2 tortitas de arroz con miel + 150 g requesón","Café + 50 g avena instantánea con miel"] },
  { slot:"Post-entreno", kcal:"~410", opts:["1-2 scoops whey + 50 g arroz inflado o 1 plátano","250 g claras + 200 g arroz/puré","Wrap integral con 150 g atún + verduras"] },
  { slot:"Cena", kcal:"~640", opts:["200 g carne/pescado, 200 g verduras al horno, arroz, aceite","Tortilla de 4 huevos + queso, ensalada con aguacate","Curry/guiso de pollo con garbanzos y verduras"] },
];
const PAUTAS = [
  ["🥩 Proteína repartida","30-50 g por toma, cada 3-4 h."],
  ["💧 Hidratación","3-4 L/día, más en guardias. Electrolitos en turnos largos."],
  ["🌾 Fibra","30-40 g/día. Verdura en cada comida + fruta."],
  ["⏱️ Timing","Carbos concentrados alrededor del entreno."],
  ["💊 Suplementos","Creatina 5 g/día, whey, vitamina D, cafeína pre-entreno."],
  ["🏥 Guardias","Lleva barritas proteicas, frutos secos, shaker y fruta."],
  ["😴 Sueño","Tu factor más frágil con turnos. Dormir poco frena la pérdida de grasa."],
  ["🍷 Alcohol","Mínimo en definición."],
];
const C = { bg:"#0c0e0b", panel:"#15170f", panel2:"#1c1f15", line:"#2a2e20", ink:"#f3f4ea", muted:"#9aa088", lime:"#cdff4a", cyan:"#4ad6ff", amber:"#ffb13d", rose:"#ff6b8a" };
const START_W = 93.9, GOAL_W = 85;
const WATER_GOAL = 14; // vasos de 250 ml ≈ 3,5 L
const todayKey = () => "log-" + new Date().toISOString().slice(0,10);
const waterKey = () => "water-" + new Date().toISOString().slice(0,10);
const uid = () => Math.random().toString(36).slice(2,9);
const fdate = (iso)=> new Date(iso).toLocaleDateString("es",{day:"2-digit",month:"short"});

async function loadKey(key,def){ try{ const r=await window.storage.get(key,false); return r?JSON.parse(r.value):def; }catch(e){ return def; } }
async function saveKey(key,val){ try{ await window.storage.set(key,JSON.stringify(val),false); }catch(e){ console.error(e); } }
async function callClaude(messages,system,maxTokens=700){
  const res=await fetch("https://api.anthropic.com/v1/messages",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({model:"claude-sonnet-4-20250514",max_tokens:maxTokens,system,messages})});
  const data=await res.json();
  return (data.content||[]).map(b=>b.type==="text"?b.text:"").join("").trim();
}
const aiErr=()=>"Se cayó la conexión. Probá de nuevo en un momento.";
const PROFILE="Bruno: hombre, 34 años, 180 cm, 93,9 kg, residente de cirugía pediátrica con guardias largas. Objetivo: definición (bajar grasa manteniendo músculo; 64,7 kg de músculo excelente, 26,2% grasa, visceral grado 9). Dieta hiperproteica.";
function seedExercises(){ const o={}; SPLIT.forEach(d=>{ o[d.key]=d.ex.map(n=>({name:n,tecnico:"",musculos:MUSCLES[n]||[]})); }); return o; }

/* ===== gráfico SVG compartido ===== */
function Chart({entries,color=C.lime,height=128}){
  if(!entries||entries.length<2) return null;
  const data=entries, W=320,H=height,pad=22;
  const ws=data.map(d=>d.w), mn=Math.min(...ws), mx=Math.max(...ws), rg=(mx-mn)||1;
  const X=i=> pad+(i/(data.length-1))*(W-2*pad);
  const Y=v=> H-pad-((v-mn)/rg)*(H-2*pad-6)-3;
  const line=data.map((d,i)=>`${X(i).toFixed(1)},${Y(d.w).toFixed(1)}`).join(" ");
  const area=`${pad},${H-pad} ${line} ${(W-pad).toFixed(1)},${H-pad}`;
  const up=data[data.length-1].w>=data[0].w, col=up?C.lime:C.amber;
  return (
    <div style={{margin:"8px 0 4px"}}>
      <div style={{fontSize:11,color:C.muted,marginBottom:3}}>Progreso · mín {mn} · máx {mx} · último {data[data.length-1].w} kg {up?"📈":"📉"}</div>
      <svg viewBox={`0 0 ${W} ${H}`} style={{width:"100%",height,display:"block"}}>
        <polygon points={area} fill={col} opacity="0.10"/>
        <polyline points={line} fill="none" stroke={col} strokeWidth="2.5" strokeLinejoin="round" strokeLinecap="round"/>
        {data.map((d,i)=>(<circle key={i} cx={X(i)} cy={Y(d.w)} r="3.2" fill={col}/>))}
      </svg>
      <div style={{display:"flex",justifyContent:"space-between",fontSize:10,color:C.muted,marginTop:-2}}><span>{fdate(data[0].date)}</span><span>{fdate(data[data.length-1].date)}</span></div>
    </div>
  );
}

export default function App(){
  const [view,setView]=useState("hoy");
  const [presetKey,setPresetKey]=useState("definicion");
  const [log,setLog]=useState([]); const [notes,setNotes]=useState([]);
  const [chat,setChat]=useState([]); const [exlog,setExlog]=useState({});
  const [exercises,setExercises]=useState(seedExercises());
  const [water,setWater]=useState(0);
  const [loaded,setLoaded]=useState(false);
  const target=PRESETS[presetKey];

  useEffect(()=>{ (async()=>{
    const prof=await loadKey("profile",{presetKey:"definicion"});
    setPresetKey(prof.presetKey||"definicion");
    setLog(await loadKey(todayKey(),[])); setNotes(await loadKey("notes",[]));
    setChat(await loadKey("chat",[])); setExlog(await loadKey("exlog",{}));
    let ex=await loadKey("exercises",null); if(!ex){ ex=seedExercises(); saveKey("exercises",ex); }
    setExercises(ex);
    setWater(await loadKey(waterKey(),0));
    setLoaded(true);
  })(); },[]);

  const changePreset=(k)=>{ setPresetKey(k); saveKey("profile",{presetKey:k}); };
  const setWaterP=(n)=>{ const v=Math.max(0,n); setWater(v); saveKey(waterKey(),v); };
  const totals=log.reduce((a,e)=>({kcal:a.kcal+(+e.kcal||0),p:a.p+(+e.proteina||0),c:a.c+(+e.carbo||0),f:a.f+(+e.grasa||0)}),{kcal:0,p:0,c:0,f:0});

  return (
    <div style={{minHeight:"100vh",background:`radial-gradient(700px 400px at 90% -10%, rgba(205,255,74,.10), transparent 60%), radial-gradient(600px 400px at -10% 10%, rgba(74,214,255,.07), transparent 55%), ${C.bg}`,color:C.ink,fontFamily:"'Manrope',system-ui,sans-serif",paddingBottom:92}}>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Manrope:wght@400;500;600;700;800&display=swap');
        *{box-sizing:border-box} ::-webkit-scrollbar{width:0}
        .disp{font-family:'Bebas Neue',sans-serif;letter-spacing:.02em;line-height:.9}
        .ph::placeholder{color:${C.muted}}
        @keyframes spin{to{transform:rotate(360deg)}}
        @keyframes pop{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
        .pop{animation:pop .35s ease both}
        textarea,input{font-family:'Manrope',sans-serif}
      `}</style>

      <div style={{maxWidth:520,margin:"0 auto",padding:"26px 16px 14px"}}>
        <div style={{display:"flex",alignItems:"center",justifyContent:"space-between"}}>
          <div>
            <div style={{fontSize:10,letterSpacing:"0.3em",textTransform:"uppercase",color:C.lime,fontWeight:800}}>Espacio IA · Bruno</div>
            <div className="disp" style={{fontSize:34,marginTop:2}}>CENTRO DE MANDO</div>
          </div>
          <div style={{width:46,height:46,borderRadius:14,background:C.panel,border:`1px solid ${C.line}`,display:"grid",placeItems:"center"}}><Flame size={22} color={C.lime}/></div>
        </div>
        <div style={{display:"flex",gap:8,marginTop:14}}>
          {Object.keys(PRESETS).map(k=>(
            <button key={k} onClick={()=>changePreset(k)} style={{flex:1,padding:"8px 4px",borderRadius:10,fontSize:12,fontWeight:700,cursor:"pointer",border:`1px solid ${presetKey===k?C.lime:C.line}`,background:presetKey===k?"rgba(205,255,74,.14)":C.panel,color:presetKey===k?C.lime:C.muted}}>{PRESETS[k].label}</button>
          ))}
        </div>
      </div>

      <div style={{maxWidth:520,margin:"0 auto",padding:"0 16px"}}>
        {view==="hoy"     && <Hoy target={target} totals={totals} log={log} setLog={setLog} loaded={loaded} water={water} setWater={setWaterP}/>}
        {view==="coach"   && <Coach chat={chat} setChat={setChat} target={target} totals={totals}/>}
        {view==="entreno" && <Entreno exlog={exlog} setExlog={setExlog} exercises={exercises} setExercises={setExercises}/>}
        {view==="reg"     && <Registro notes={notes} setNotes={setNotes} target={target}/>}
        {view==="plan"    && <Plan presetKey={presetKey}/>}
      </div>

      <div style={{position:"fixed",bottom:0,left:0,right:0,background:"rgba(12,14,11,.92)",backdropFilter:"blur(10px)",borderTop:`1px solid ${C.line}`}}>
        <div style={{maxWidth:520,margin:"0 auto",display:"flex"}}>
          {[["hoy","Hoy",Utensils],["coach","Coach",MessageSquare],["entreno","Entreno",Dumbbell],["reg","Registro",NotebookPen],["plan","Plan",ClipboardList]].map(([k,lbl,Ic])=>(
            <button key={k} onClick={()=>setView(k)} style={{flex:1,background:"none",border:"none",cursor:"pointer",padding:"12px 0 16px",display:"flex",flexDirection:"column",alignItems:"center",gap:4,color:view===k?C.lime:C.muted}}>
              <Ic size={19}/><span style={{fontSize:10,fontWeight:700}}>{lbl}</span>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

function AIPanel({title,busy,text,color=C.lime}){
  if(!busy && !text) return null;
  return (
    <div className="pop" style={{background:"rgba(205,255,74,.05)",border:`1px solid ${C.line}`,borderLeft:`3px solid ${color}`,borderRadius:12,padding:"13px 15px",marginTop:10}}>
      <div style={{display:"flex",alignItems:"center",gap:7,fontSize:11,fontWeight:800,letterSpacing:".08em",textTransform:"uppercase",color,marginBottom:busy?0:7}}><Sparkles size={13}/>{title}</div>
      {busy?<div style={{display:"flex",gap:7,alignItems:"center",color:C.muted,fontSize:13,marginTop:7}}><Loader2 size={14} style={{animation:"spin 1s linear infinite"}}/>pensando…</div>
           :<div style={{fontSize:13.5,lineHeight:1.55,whiteSpace:"pre-wrap",color:"#dde0cf"}}>{text}</div>}
    </div>
  );
}

/* ===================== HOY ===================== */
function Bar({icon:Ic,label,val,max,unit,color}){
  const pct=Math.min(100,max?(val/max)*100:0); const over=val>max;
  return (
    <div style={{background:C.panel,border:`1px solid ${over?C.amber:C.line}`,borderRadius:14,padding:"13px 15px",marginBottom:10}}>
      <div style={{display:"flex",alignItems:"center",justifyContent:"space-between",marginBottom:8}}>
        <span style={{display:"flex",alignItems:"center",gap:8,fontSize:13,fontWeight:700}}><Ic size={16} color={color}/>{label}</span>
        <span style={{fontVariantNumeric:"tabular-nums",fontSize:13,color:over?C.amber:C.muted}}><b style={{color:over?C.amber:C.ink,fontSize:15}}>{Math.round(val)}</b> / {max} {unit}</span>
      </div>
      <div style={{height:8,background:C.panel2,borderRadius:6,overflow:"hidden"}}><div style={{height:"100%",width:pct+"%",background:over?C.amber:color,borderRadius:6,transition:"width .5s"}}/></div>
    </div>
  );
}
function Hoy({target,totals,log,setLog,loaded,water,setWater}){
  const [text,setText]=useState(""); const [busy,setBusy]=useState(false); const [err,setErr]=useState("");
  const fileRef=useRef();
  const [aiBusy,setAiBusy]=useState(""); const [aiTitle,setAiTitle]=useState(""); const [aiText,setAiText]=useState(""); const [showMoments,setShowMoments]=useState(false);
  const rem={kcal:Math.max(0,target.kcal-totals.kcal),p:Math.max(0,target.p-totals.p),c:Math.max(0,target.c-totals.c),f:Math.max(0,target.f-totals.f)};
  const FOOD_SYS="Eres un nutricionista experto. Estima los macros TOTALES sumados de lo que comió el usuario. Responde ÚNICAMENTE un JSON válido sin markdown ni texto: {\"resumen\":string corto,\"kcal\":number,\"proteina\":number,\"carbo\":number,\"grasa\":number}. Gramos enteros.";
  const pushEntry=(o,fb)=>{ const e={id:uid(),resumen:o.resumen||fb,kcal:+o.kcal||0,proteina:+o.proteina||0,carbo:+o.carbo||0,grasa:+o.grasa||0,t:Date.now()}; const next=[e,...log]; setLog(next); saveKey(todayKey(),next); };
  const addFood=async()=>{ if(!text.trim()||busy)return; setBusy(true); setErr(""); const d=text.trim();
    try{ const out=await callClaude([{role:"user",content:d}],FOOD_SYS,400); pushEntry(JSON.parse(out.replace(/```json|```/g,"").trim()),d); setText(""); }
    catch(e){ setErr("No pude estimar eso. Añade cantidades (ej. '200 g pollo, 150 g arroz')."); } setBusy(false); };
  const onPhoto=async(e)=>{ const file=e.target.files&&e.target.files[0]; if(!file)return; setBusy(true); setErr("");
    try{ const b64=await new Promise((res,rej)=>{const r=new FileReader();r.onload=()=>res(r.result.split(",")[1]);r.onerror=rej;r.readAsDataURL(file);});
      const media=["image/jpeg","image/png","image/gif","image/webp"].includes(file.type)?file.type:"image/jpeg";
      const out=await callClaude([{role:"user",content:[{type:"image",source:{type:"base64",media_type:media,data:b64}},{type:"text",text:"Estima los macros totales de la comida de esta foto."}]}],FOOD_SYS,400);
      pushEntry(JSON.parse(out.replace(/```json|```/g,"").trim()),"Comida (foto)"); }
    catch(err){ setErr("No pude leer la foto. Prueba con más luz o por texto."); } setBusy(false); e.target.value=""; };
  const del=(id)=>{ const next=log.filter(e=>e.id!==id); setLog(next); saveKey(todayKey(),next); };
  const run=async(title,sys,user,max=600)=>{ setShowMoments(false); setAiBusy(title); setAiTitle(title); setAiText("");
    try{ setAiText(await callClaude([{role:"user",content:user}],sys,max)||"…"); }catch(e){ setAiText(aiErr()); } setAiBusy(""); };
  const suggestDinner=()=>run("Cena sugerida",`${PROFILE} Plan: ${target.kcal} kcal, ${target.p}P/${target.c}C/${target.f}G. Español, breve, sin preámbulo.`,`Hoy le quedan: ${rem.kcal} kcal, ${rem.p} g proteína, ${rem.c} g carbo, ${rem.f} g grasa. Propón 2-3 cenas concretas con cantidades que cierren esos macros, priorizando proteína.`);
  const whatNow=(m)=>run("¿Qué como ahora?",`${PROFILE} Plan: ${target.kcal} kcal, ${target.p}P/${target.c}C/${target.f}G. Español, breve.`,`Necesita una opción para: ${m}. Le quedan ${rem.kcal} kcal, ${rem.p} g prot, ${rem.c} g carbo, ${rem.f} g grasa. 1-2 opciones concretas con cantidades.`);
  const daySummary=()=>{ const det=log.map(e=>`${e.resumen} (${Math.round(e.kcal)}kcal P${Math.round(e.proteina)})`).join("; ")||"nada"; run("Resumen del día",`${PROFILE} Objetivo: ${target.kcal} kcal, ${target.p}P/${target.c}C/${target.f}G. Español, honesto, breve.`,`Hoy comió: ${det}. Totales: ${Math.round(totals.kcal)} kcal, P${Math.round(totals.p)} C${Math.round(totals.c)} G${Math.round(totals.f)}. Resumen corto: ¿pegó los macros? ¿qué faltó? consejo para mañana.`); };
  const chip=(a)=>({padding:"9px 8px",borderRadius:10,fontSize:12,fontWeight:700,cursor:"pointer",border:`1px solid ${a?C.lime:C.line}`,background:a?"rgba(205,255,74,.12)":C.panel,color:a?C.lime:C.ink,display:"flex",alignItems:"center",justifyContent:"center",gap:6,flex:1});
  const liters=(water*0.25).toFixed(2);
  return (
    <div className="pop">
      <Bar icon={Flame} label="Calorías" val={totals.kcal} max={target.kcal} unit="kcal" color={C.lime}/>
      <Bar icon={Beef} label="Proteína" val={totals.p} max={target.p} unit="g" color={C.cyan}/>
      <Bar icon={Wheat} label="Carbos" val={totals.c} max={target.c} unit="g" color={C.lime}/>
      <Bar icon={Droplet} label="Grasa" val={totals.f} max={target.f} unit="g" color={C.amber}/>
      <div style={{background:"rgba(74,214,255,.08)",border:"1px solid rgba(74,214,255,.3)",borderRadius:12,padding:"10px 14px",margin:"4px 0 12px",fontSize:12.5,color:"#cfe9f5"}}>Te quedan <b style={{color:C.cyan}}>{rem.p} g de proteína</b> hoy. La prioridad.</div>

      {/* Hidratación */}
      <div style={{background:C.panel,border:`1px solid ${C.line}`,borderRadius:14,padding:"13px 15px",marginBottom:14}}>
        <div style={{display:"flex",alignItems:"center",justifyContent:"space-between",marginBottom:8}}>
          <span style={{display:"flex",alignItems:"center",gap:8,fontSize:13,fontWeight:700}}><GlassWater size={16} color={C.cyan}/>Hidratación</span>
          <span style={{fontSize:13,color:C.muted}}><b style={{color:C.ink,fontSize:15}}>{liters}</b> / 3,5 L</span>
        </div>
        <div style={{display:"flex",alignItems:"center",gap:8}}>
          <button onClick={()=>setWater(water-1)} style={{width:38,height:38,borderRadius:10,border:`1px solid ${C.line}`,background:C.panel2,color:C.ink,cursor:"pointer",display:"grid",placeItems:"center"}}><Minus size={16}/></button>
          <div style={{flex:1,display:"flex",gap:3}}>{Array.from({length:WATER_GOAL}).map((_,i)=>(<div key={i} style={{flex:1,height:22,borderRadius:5,background:i<water?C.cyan:C.panel2,border:`1px solid ${i<water?C.cyan:C.line}`,transition:"all .2s"}}/>))}</div>
          <button onClick={()=>setWater(water+1)} style={{width:38,height:38,borderRadius:10,border:"none",background:C.cyan,color:"#04212b",cursor:"pointer",display:"grid",placeItems:"center"}}><Plus size={16}/></button>
        </div>
      </div>

      <div style={{display:"flex",gap:7,marginBottom:7}}>
        <button onClick={suggestDinner} style={chip(aiBusy==="Cena sugerida")}><ChefHat size={14}/>Sugerir cena</button>
        <button onClick={()=>setShowMoments(v=>!v)} style={chip(showMoments)}><Clock size={14}/>¿Qué como ahora?</button>
      </div>
      {showMoments && <div className="pop" style={{display:"flex",gap:7,flexWrap:"wrap",marginBottom:7}}>{["Pre-entreno","Post-entreno","En guardia","Desayuno rápido"].map(m=>(<button key={m} onClick={()=>whatNow(m)} style={{...chip(false),flex:"1 1 45%",fontSize:11.5,padding:"8px 6px"}}>{m}</button>))}</div>}
      <button onClick={daySummary} style={{...chip(aiBusy==="Resumen del día"),width:"100%",marginBottom:2}}><Sparkles size={14}/>Resumen IA del día</button>
      <AIPanel title={aiTitle} busy={!!aiBusy} text={aiText}/>

      <div style={{background:C.panel,border:`1px solid ${C.line}`,borderRadius:16,padding:14,marginTop:16}}>
        <div style={{fontSize:13,fontWeight:800,marginBottom:8,display:"flex",alignItems:"center",gap:8}}><Plus size={16} color={C.lime}/>Registrar comida</div>
        <textarea value={text} onChange={e=>setText(e.target.value)} className="ph" rows={2} placeholder="Ej: 200 g pollo a la plancha, 150 g arroz, ensalada…" style={{width:"100%",resize:"none",background:C.panel2,border:`1px solid ${C.line}`,borderRadius:10,padding:"10px 12px",color:C.ink,fontSize:13.5,outline:"none"}}/>
        <div style={{display:"flex",gap:8,marginTop:8}}>
          <button onClick={addFood} disabled={busy} style={{flex:1,padding:"11px",borderRadius:10,border:"none",cursor:"pointer",background:busy?C.panel2:C.lime,color:busy?C.muted:"#1a2400",fontWeight:800,fontSize:14,display:"flex",alignItems:"center",justifyContent:"center",gap:8}}>{busy?<><Loader2 size={16} style={{animation:"spin 1s linear infinite"}}/>Estimando…</>:"Añadir con IA"}</button>
          <button onClick={()=>fileRef.current.click()} disabled={busy} style={{width:52,borderRadius:10,border:`1px solid ${C.line}`,background:C.panel2,color:C.lime,cursor:"pointer",display:"grid",placeItems:"center"}}><Camera size={20}/></button>
          <input ref={fileRef} type="file" accept="image/*" capture="environment" onChange={onPhoto} style={{display:"none"}}/>
        </div>
        {err && <div style={{color:C.rose,fontSize:12,marginTop:8}}>{err}</div>}
      </div>

      <div style={{marginTop:18,marginBottom:6,display:"flex",justifyContent:"space-between",alignItems:"baseline"}}><span className="disp" style={{fontSize:22,color:C.lime}}>HOY</span><span style={{fontSize:12,color:C.muted}}>{log.length} {log.length===1?"registro":"registros"}</span></div>
      {!loaded && <div style={{color:C.muted,fontSize:13,padding:"10px 0"}}>Cargando…</div>}
      {loaded && log.length===0 && <div style={{color:C.muted,fontSize:13,padding:"18px 0",textAlign:"center"}}>Aún no registras nada hoy.</div>}
      {log.map(e=>(
        <div key={e.id} className="pop" style={{background:C.panel,border:`1px solid ${C.line}`,borderRadius:13,padding:"11px 14px",marginBottom:9,display:"flex",gap:10,alignItems:"flex-start"}}>
          <div style={{flex:1}}><div style={{fontSize:13.5,fontWeight:600,marginBottom:4}}>{e.resumen}</div>
            <div style={{fontSize:11.5,color:C.muted,display:"flex",gap:10,flexWrap:"wrap",fontVariantNumeric:"tabular-nums"}}><span style={{color:C.lime}}>{Math.round(e.kcal)} kcal</span><span style={{color:C.cyan}}>P {Math.round(e.proteina)}</span><span>C {Math.round(e.carbo)}</span><span style={{color:C.amber}}>G {Math.round(e.grasa)}</span></div></div>
          <button onClick={()=>del(e.id)} style={{background:"none",border:"none",cursor:"pointer",color:C.muted}}><Trash2 size={16}/></button>
        </div>
      ))}
    </div>
  );
}

/* ===================== COACH ===================== */
function Coach({chat,setChat,target,totals}){
  const [text,setText]=useState(""); const [busy,setBusy]=useState(false); const endRef=useRef(null);
  useEffect(()=>{ endRef.current&&endRef.current.scrollIntoView({behavior:"smooth"}); },[chat,busy]);
  const send=async()=>{ if(!text.trim()||busy)return; const next=[...chat,{role:"user",content:text.trim()}]; setChat(next); setText(""); setBusy(true);
    try{ const sys=`Eres el coach nutricional y de fuerza de Bruno. ${PROFILE} Plan: ${target.kcal} kcal, ${target.p}P/${target.c}C/${target.f}G. Split de 4 días: A Pecho+Bíceps, B Pierna cuádriceps + Hombros (mismo día), C Espalda+Tríceps, D Pierna posterior. Hoy lleva: ${Math.round(totals.kcal)} kcal, P${Math.round(totals.p)} C${Math.round(totals.c)} G${Math.round(totals.f)}. Español, directo y técnico pero claro, pocas frases, sin listas largas. Honesto, no le hagas la pelota. No eres médico: recuérdalo solo si pregunta algo clínico serio.`;
      const out=await callClaude(next.slice(-12).map(m=>({role:m.role,content:m.content})),sys,700); const fin=[...next,{role:"assistant",content:out||"…"}]; setChat(fin); saveKey("chat",fin.slice(-40)); }
    catch(e){ setChat([...next,{role:"assistant",content:aiErr()}]); } setBusy(false); };
  return (
    <div className="pop" style={{display:"flex",flexDirection:"column",height:"calc(100vh - 232px)",minHeight:380}}>
      <div style={{flex:1,overflowY:"auto",paddingBottom:8}}>
        {chat.length===0 && (<div style={{textAlign:"center",color:C.muted,fontSize:13,padding:"30px 14px"}}><MessageSquare size={26} color={C.lime} style={{marginBottom:10}}/><p>Tu coach conoce tu plan, tu split y lo que llevas comido hoy.</p>
          <div style={{display:"flex",flexDirection:"column",gap:8,marginTop:16}}>{["¿Qué ceno para llegar a mi proteína?","¿Cómo como en una guardia de 24 h?","Me salté el pre-entreno, ¿qué hago?"].map(q=>(<button key={q} onClick={()=>setText(q)} style={{background:C.panel,border:`1px solid ${C.line}`,borderRadius:10,padding:"9px 12px",color:C.ink,fontSize:12.5,cursor:"pointer",textAlign:"left"}}>{q}</button>))}</div></div>)}
        {chat.map((m,i)=>(<div key={i} className="pop" style={{display:"flex",justifyContent:m.role==="user"?"flex-end":"flex-start",marginBottom:10}}><div style={{maxWidth:"85%",padding:"10px 13px",borderRadius:14,fontSize:13.5,lineHeight:1.5,whiteSpace:"pre-wrap",background:m.role==="user"?C.lime:C.panel,color:m.role==="user"?"#1a2400":C.ink,border:m.role==="user"?"none":`1px solid ${C.line}`,borderBottomRightRadius:m.role==="user"?4:14,borderBottomLeftRadius:m.role==="user"?14:4}}>{m.content}</div></div>))}
        {busy && <div style={{display:"flex",gap:6,color:C.muted,fontSize:13,alignItems:"center",padding:"4px 2px"}}><Loader2 size={15} style={{animation:"spin 1s linear infinite"}}/>pensando…</div>}
        <div ref={endRef}/>
      </div>
      <div style={{display:"flex",gap:8,paddingTop:6}}>
        <input value={text} onChange={e=>setText(e.target.value)} onKeyDown={e=>{if(e.key==="Enter")send();}} className="ph" placeholder="Pregúntale a tu coach…" style={{flex:1,background:C.panel,border:`1px solid ${C.line}`,borderRadius:12,padding:"12px 14px",color:C.ink,fontSize:14,outline:"none"}}/>
        <button onClick={send} disabled={busy} style={{width:48,borderRadius:12,border:"none",background:C.lime,color:"#1a2400",cursor:"pointer",display:"grid",placeItems:"center"}}><Send size={18}/></button>
      </div>
    </div>
  );
}

/* ===================== ENTRENO ===================== */
function Entreno({exlog,setExlog,exercises,setExercises}){
  const [sel,setSel]=useState("B"); const [open,setOpen]=useState(null);
  const [w,setW]=useState(""); const [reps,setReps]=useState("");
  const [dayBusy,setDayBusy]=useState(false); const [daySug,setDaySug]=useState("");
  const [progBusy,setProgBusy]=useState(""); const [prog,setProg]=useState({});
  const [adding,setAdding]=useState(false); const [addMode,setAddMode]=useState("nombre"); const [addText,setAddText]=useState(""); const [addBusy,setAddBusy]=useState(false); const [addErr,setAddErr]=useState("");
  const [wkBusy,setWkBusy]=useState(false); const [wk,setWk]=useState("");

  const dayObj=SPLIT.find(d=>d.key===sel)||{name:"Día "+sel,fuel:""};
  const dayExs=exercises[sel]||[];
  const dayMuscles=[...new Set(dayExs.flatMap(e=>e.musculos||[]))];
  const last=(n)=>{ const a=exlog[n]; return a&&a.length?a[0]:null; };
  const chartData=(n)=> (exlog[n]||[]).slice().reverse().map(s=>({date:s.date,w:s.w}));
  const saveExs=(nx)=>{ setExercises(nx); saveKey("exercises",nx); };

  // volumen últimos 7 días por músculo
  const exMap={}; Object.values(exercises).flat().forEach(e=>{ exMap[e.name]=e.musculos||[]; });
  const weekAgo=Date.now()-7*864e5; const vol={};
  Object.entries(exlog).forEach(([name,sets])=>{ const ms=exMap[name]||MUSCLES[name]||[]; (sets||[]).forEach(s=>{ if(new Date(s.date).getTime()>=weekAgo) ms.forEach(m=>{ vol[m]=(vol[m]||0)+1; }); }); });
  const volArr=Object.entries(vol).sort((a,b)=>b[1]-a[1]); const volMax=volArr.length?volArr[0][1]:1;

  const addSet=(n)=>{ if(!w.trim())return; const e={date:new Date().toISOString(),w:parseFloat(w),reps:reps.trim()||"-"}; const next={...exlog,[n]:[e,...(exlog[n]||[])].slice(0,60)}; setExlog(next); saveKey("exlog",next); setW(""); setReps(""); };
  const delSet=(n,i)=>{ const arr=[...(exlog[n]||[])]; arr.splice(i,1); const next={...exlog,[n]:arr}; setExlog(next); saveKey("exlog",next); };
  const delExercise=(n)=>{ saveExs({...exercises,[sel]:dayExs.filter(e=>e.name!==n)}); };

  const addExercise=async()=>{ if(!addText.trim()||addBusy)return; setAddBusy(true); setAddErr("");
    try{
      if(addMode==="nombre"){
        const sys="Eres entrenador. Para el ejercicio dado responde SOLO JSON {\"tecnico\":string (nombre técnico/formal; vacío si no aplica),\"musculos\":[string]} con músculos principales, nombres cortos en español.";
        const o=JSON.parse((await callClaude([{role:"user",content:addText.trim()}],sys,250)).replace(/```json|```/g,"").trim());
        saveExs({...exercises,[sel]:[...dayExs,{name:addText.trim(),tecnico:o.tecnico||"",musculos:o.musculos||[]}]});
      } else {
        const sys="El usuario describe un ejercicio que no sabe nombrar. Identifícalo. Responde SOLO JSON {\"nombre\":string (nombre común español),\"tecnico\":string (nombre técnico/formal),\"musculos\":[string]}. Nombres cortos.";
        const o=JSON.parse((await callClaude([{role:"user",content:addText.trim()}],sys,300)).replace(/```json|```/g,"").trim());
        saveExs({...exercises,[sel]:[...dayExs,{name:o.nombre||addText.trim().slice(0,40),tecnico:o.tecnico||"",musculos:o.musculos||[]}]});
      }
      setAddText(""); setAdding(false);
    }catch(e){ setAddErr("No pude procesarlo. Sé más específico o intenta de nuevo."); }
    setAddBusy(false);
  };
  const analyzeProg=async(ex)=>{ setProgBusy(ex.name);
    const hist=(exlog[ex.name]||[]).slice(0,8).map(s=>`${fdate(s.date)} ${s.w}kg×${s.reps}`).join(" | ")||"sin registros";
    try{ const sys=`Eres el entrenador de Bruno. ${PROFILE} Español, directo, breve.`;
      const out=await callClaude([{role:"user",content:`Ejercicio: ${ex.name}${ex.tecnico?" ("+ex.tecnico+")":""}. Músculos: ${(ex.musculos||[]).join(", ")||"?"}. Historial (nuevo→viejo): ${hist}. Analiza el progreso y da recomendaciones concretas (carga, reps, técnica). Breve.`}],sys,400);
      setProg(p=>({...p,[ex.name]:out})); }
    catch(e){ setProg(p=>({...p,[ex.name]:aiErr()})); } setProgBusy("");
  };
  const suggest=async()=>{ setDayBusy(true); setDaySug("");
    const hist=dayExs.map(ex=>{ const a=(exlog[ex.name]||[]).slice(0,3).map(s=>`${s.w}kg×${s.reps}`).join(", "); return a?`${ex.name}: ${a}`:`${ex.name}: sin registro`; }).join(" | ");
    try{ const sys=`Eres el entrenador de fuerza de Bruno. ${PROFILE} Split de 4 días: A Pecho+Bíceps, B Pierna cuádriceps + Hombros, C Espalda+Tríceps, D Pierna posterior. Mantén su orden. Español, directo.`;
      setDaySug(await callClaude([{role:"user",content:`Día ${sel}: ${dayObj.name}. Músculos del día: ${dayMuscles.join(", ")}. Historial: ${hist}. Dame la sesión en orden y progresión concreta donde haya datos. Breve.`}],sys,800)); }
    catch(e){ setDaySug(aiErr()); } setDayBusy(false);
  };
  const planWeek=async()=>{ setWkBusy(true); setWk("");
    try{ const sys=`Eres el entrenador de Bruno. ${PROFILE} Split de 4 días: A Pecho+Bíceps, B Pierna cuádriceps + Hombros, C Espalda+Tríceps, D Pierna posterior. Español, breve.`;
      setWk(await callClaude([{role:"user",content:"Propón una distribución semanal (7 días) de estos 4 entrenamientos + descansos, pensada para alguien con guardias impredecibles. Incluye una versión 'plan A' fija y un consejo para reordenar si cae una guardia. Formato día: entreno, breve."}],sys,500)); }
    catch(e){ setWk(aiErr()); } setWkBusy(false);
  };
  const tag={fontSize:10.5,fontWeight:700,padding:"3px 8px",borderRadius:999,background:"rgba(74,214,255,.12)",color:C.cyan};

  return (
    <div className="pop">
      <div className="disp" style={{fontSize:24,color:C.lime,marginBottom:10}}>TU SPLIT · 4 DÍAS</div>

      {/* volumen semanal por músculo */}
      {volArr.length>0 && (
        <div style={{background:C.panel,border:`1px solid ${C.line}`,borderRadius:14,padding:"14px 16px",marginBottom:12}}>
          <div style={{display:"flex",alignItems:"center",gap:8,fontSize:12.5,fontWeight:800,marginBottom:10}}><Activity size={15} color={C.lime}/>Volumen · últimos 7 días <span style={{color:C.muted,fontWeight:500,fontSize:11}}>(registros por músculo)</span></div>
          {volArr.slice(0,8).map(([m,n])=>(
            <div key={m} style={{display:"flex",alignItems:"center",gap:10,marginBottom:6}}>
              <span style={{fontSize:11.5,color:C.muted,width:96,flexShrink:0}}>{m}</span>
              <div style={{flex:1,height:7,background:C.panel2,borderRadius:5,overflow:"hidden"}}><div style={{height:"100%",width:(n/volMax*100)+"%",background:C.lime,borderRadius:5}}/></div>
              <span style={{fontSize:11.5,color:C.ink,fontWeight:700,width:18,textAlign:"right"}}>{n}</span>
            </div>
          ))}
        </div>
      )}

      <div style={{display:"flex",gap:6,marginBottom:14}}>
        {SPLIT.map(d=>(<button key={d.key} onClick={()=>{setSel(d.key);setDaySug("");setOpen(null);setAdding(false);}} style={{width:44,height:44,borderRadius:11,fontFamily:"'Bebas Neue'",fontSize:22,cursor:"pointer",border:`1px solid ${sel===d.key?C.lime:C.line}`,background:sel===d.key?"rgba(205,255,74,.14)":C.panel,color:sel===d.key?C.lime:C.muted}}>{d.key}</button>))}
      </div>
      <div style={{background:C.panel,border:`1px solid ${C.line}`,borderRadius:16,padding:"14px 16px",marginBottom:12}}>
        <div style={{display:"flex",justifyContent:"space-between",alignItems:"baseline"}}><div className="disp" style={{fontSize:24}}>{dayObj.name.toUpperCase()}</div><span style={{fontSize:11,color:C.muted,fontWeight:700}}>{dayObj.fuel}</span></div>
        {dayMuscles.length>0 && <div style={{display:"flex",gap:6,flexWrap:"wrap",marginTop:8}}>{dayMuscles.map(m=>(<span key={m} style={tag}>{m}</span>))}</div>}
      </div>

      {dayExs.map(ex=>{ const isOpen=open===ex.name; const l=last(ex.name); const cd=chartData(ex.name);
        return (
          <div key={ex.name} style={{background:C.panel,border:`1px solid ${isOpen?C.lime:C.line}`,borderRadius:13,marginBottom:9,overflow:"hidden"}}>
            <button onClick={()=>{setOpen(isOpen?null:ex.name);setW("");setReps("");}} style={{width:"100%",background:"none",border:"none",cursor:"pointer",padding:"12px 14px",display:"flex",alignItems:"center",gap:10,color:C.ink,textAlign:"left"}}>
              <div style={{flex:1}}>
                <div style={{fontSize:13.5,fontWeight:600}}>{ex.name}</div>
                {ex.tecnico && <div style={{fontSize:11,color:C.muted,fontStyle:"italic"}}>{ex.tecnico}</div>}
                {l ? <div style={{fontSize:11.5,color:C.cyan,marginTop:2}}>última: {l.w} kg × {l.reps} · {fdate(l.date)}</div>
                   : <div style={{fontSize:11.5,color:C.muted,marginTop:2}}>{(ex.musculos||[]).join(" · ")}</div>}
              </div>
              <span style={{color:C.muted,fontSize:14}}>{isOpen?"▴":"▾"}</span>
            </button>
            {isOpen && (
              <div className="pop" style={{padding:"0 14px 14px"}}>
                {(ex.musculos||[]).length>0 && <div style={{display:"flex",gap:6,flexWrap:"wrap",marginBottom:10}}>{ex.musculos.map(m=>(<span key={m} style={tag}>{m}</span>))}</div>}
                <div style={{display:"flex",gap:8,marginBottom:8}}>
                  <input value={w} onChange={e=>setW(e.target.value)} type="number" inputMode="decimal" className="ph" placeholder="kg" style={{flex:1,background:C.panel2,border:`1px solid ${C.line}`,borderRadius:9,padding:"9px 11px",color:C.ink,fontSize:14,outline:"none"}}/>
                  <input value={reps} onChange={e=>setReps(e.target.value)} className="ph" placeholder="reps (ej. 3x8)" style={{flex:1.3,background:C.panel2,border:`1px solid ${C.line}`,borderRadius:9,padding:"9px 11px",color:C.ink,fontSize:14,outline:"none"}}/>
                  <button onClick={()=>addSet(ex.name)} style={{width:44,borderRadius:9,border:"none",background:C.lime,color:"#1a2400",cursor:"pointer",fontSize:20}}>＋</button>
                </div>
                <Chart entries={cd}/>
                {(exlog[ex.name]||[]).length===0 && <div style={{fontSize:12,color:C.muted,padding:"4px 0"}}>Sin registros. Anota tu peso al hacerlo.</div>}
                {(exlog[ex.name]||[]).map((s,i)=>(
                  <div key={i} style={{display:"flex",alignItems:"center",gap:10,padding:"7px 0",borderTop:`1px solid ${C.line}`}}>
                    <span style={{fontSize:12.5,color:C.muted,minWidth:54}}>{fdate(s.date)}</span><span style={{fontSize:13.5,fontWeight:600}}>{s.w} kg</span><span style={{fontSize:13,color:C.muted}}>× {s.reps}</span>
                    <button onClick={()=>delSet(ex.name,i)} style={{marginLeft:"auto",background:"none",border:"none",cursor:"pointer",color:C.muted}}><Trash2 size={14}/></button>
                  </div>
                ))}
                <div style={{display:"flex",gap:8,marginTop:10}}>
                  <button onClick={()=>analyzeProg(ex)} disabled={progBusy===ex.name} style={{flex:1,padding:"9px",borderRadius:9,border:`1px solid ${C.line}`,background:C.panel2,color:C.lime,cursor:"pointer",fontWeight:700,fontSize:12.5,display:"flex",alignItems:"center",justifyContent:"center",gap:6}}>{progBusy===ex.name?<><Loader2 size={13} style={{animation:"spin 1s linear infinite"}}/>Analizando…</>:<><Sparkles size={13}/>Progreso y recomendaciones</>}</button>
                  <button onClick={()=>delExercise(ex.name)} style={{padding:"9px 12px",borderRadius:9,border:`1px solid ${C.line}`,background:"none",color:C.muted,cursor:"pointer",fontSize:12.5}}>Quitar</button>
                </div>
                {prog[ex.name] && <AIPanel title="Progreso" busy={false} text={prog[ex.name]} color={C.cyan}/>}
              </div>
            )}
          </div>
        );
      })}

      {!adding ? (
        <button onClick={()=>{setAdding(true);setAddErr("");setAddText("");}} style={{width:"100%",padding:"11px",borderRadius:12,border:`1px dashed ${C.line}`,background:"none",color:C.muted,cursor:"pointer",fontWeight:700,fontSize:13,marginTop:4}}>＋ Añadir ejercicio nuevo</button>
      ) : (
        <div className="pop" style={{background:C.panel,border:`1px solid ${C.lime}`,borderRadius:14,padding:14,marginTop:4}}>
          <div style={{display:"flex",gap:7,marginBottom:10}}>
            <button onClick={()=>setAddMode("nombre")} style={{flex:1,padding:"8px",borderRadius:9,fontSize:12,fontWeight:700,cursor:"pointer",border:`1px solid ${addMode==="nombre"?C.lime:C.line}`,background:addMode==="nombre"?"rgba(205,255,74,.12)":"transparent",color:addMode==="nombre"?C.lime:C.muted}}>Sé el nombre</button>
            <button onClick={()=>setAddMode("describir")} style={{flex:1,padding:"8px",borderRadius:9,fontSize:12,fontWeight:700,cursor:"pointer",border:`1px solid ${addMode==="describir"?C.lime:C.line}`,background:addMode==="describir"?"rgba(205,255,74,.12)":"transparent",color:addMode==="describir"?C.lime:C.muted}}>Describirlo</button>
          </div>
          <textarea value={addText} onChange={e=>setAddText(e.target.value)} rows={addMode==="describir"?3:1} className="ph" placeholder={addMode==="nombre"?"Ej: Hip thrust con barra":"Ej: máquina sentado, empujo dos agarres hacia afuera abriendo los brazos…"} style={{width:"100%",resize:"none",background:C.panel2,border:`1px solid ${C.line}`,borderRadius:10,padding:"10px 12px",color:C.ink,fontSize:13.5,outline:"none"}}/>
          <div style={{display:"flex",gap:8,marginTop:8}}>
            <button onClick={addExercise} disabled={addBusy} style={{flex:1,padding:"10px",borderRadius:10,border:"none",background:addBusy?C.panel2:C.lime,color:addBusy?C.muted:"#1a2400",cursor:"pointer",fontWeight:800,fontSize:13.5,display:"flex",alignItems:"center",justifyContent:"center",gap:6}}>{addBusy?<><Loader2 size={14} style={{animation:"spin 1s linear infinite"}}/>Identificando…</>:(addMode==="nombre"?"Añadir y analizar músculos":"Identificar y añadir")}</button>
            <button onClick={()=>setAdding(false)} style={{padding:"10px 14px",borderRadius:10,border:`1px solid ${C.line}`,background:"none",color:C.muted,cursor:"pointer",fontSize:13.5}}>Cancelar</button>
          </div>
          {addErr && <div style={{color:C.rose,fontSize:12,marginTop:8}}>{addErr}</div>}
        </div>
      )}

      <button onClick={suggest} disabled={dayBusy} style={{width:"100%",marginTop:12,padding:"12px",borderRadius:12,border:"none",cursor:"pointer",background:dayBusy?C.panel2:C.lime,color:dayBusy?C.muted:"#1a2400",fontWeight:800,fontSize:14,display:"flex",alignItems:"center",justifyContent:"center",gap:8}}>{dayBusy?<><Loader2 size={16} style={{animation:"spin 1s linear infinite"}}/>Armando sesión…</>:<><Sparkles size={16}/>Sugerencia IA del día completo</>}</button>
      <AIPanel title={`Sesión ${sel} · ${dayObj.name}`} busy={dayBusy} text={daySug}/>

      <button onClick={planWeek} disabled={wkBusy} style={{width:"100%",marginTop:10,padding:"11px",borderRadius:12,border:`1px solid ${C.line}`,cursor:"pointer",background:C.panel,color:C.lime,fontWeight:800,fontSize:13.5,display:"flex",alignItems:"center",justifyContent:"center",gap:8}}>{wkBusy?<><Loader2 size={15} style={{animation:"spin 1s linear infinite"}}/>Planificando…</>:<><CalendarDays size={16}/>Planificar mi semana (IA)</>}</button>
      <AIPanel title="Plan semanal" busy={wkBusy} text={wk} color={C.cyan}/>
    </div>
  );
}

/* ===================== REGISTRO ===================== */
function Registro({notes,setNotes,target}){
  const [type,setType]=useState("peso"); const [text,setText]=useState(""); const [weight,setWeight]=useState("");
  const [busy,setBusy]=useState(false); const [trend,setTrend]=useState("");
  const TYPES={ peso:["Peso",C.cyan], entreno:["Entreno",C.lime], sensacion:["Cómo me siento",C.amber], nota:["Nota",C.muted] };
  const add=()=>{ if(type==="peso"&&!weight.trim())return; if(type!=="peso"&&!text.trim())return; const e={id:uid(),type,date:new Date().toISOString(),text:type==="peso"?`${weight} kg`:text.trim(),weight:type==="peso"?parseFloat(weight):null}; const next=[e,...notes]; setNotes(next); saveKey("notes",next); setText(""); setWeight(""); };
  const del=(id)=>{ const next=notes.filter(n=>n.id!==id); setNotes(next); saveKey("notes",next); };
  const weights=notes.filter(n=>n.type==="peso"&&n.weight).slice().reverse();
  const lastW=weights.length?weights[weights.length-1].weight:START_W;
  const startW=weights.length?weights[0].weight:START_W;
  const chartW=weights.map(x=>({date:x.date,w:x.weight}));
  const goalPct=Math.max(0,Math.min(100,((startW-lastW)/((startW-GOAL_W)||1))*100));
  const toGoal=(lastW-GOAL_W);
  const analyze=async()=>{ setBusy(true); setTrend(""); const series=weights.map(w=>`${fdate(w.date)}: ${w.weight}kg`).join(" → ")||"sin datos";
    try{ const sys=`Eres el coach de Bruno. ${PROFILE} Déficit a ${target.kcal} kcal buscando ~0,4-0,5 kg/sem de grasa sin perder músculo, hacia ~85 kg. Español, honesto, breve.`;
      setTrend(await callClaude([{role:"user",content:`Registro de peso: ${series}. Analiza la tendencia: ¿ritmo correcto? ¿ajustar calorías y cómo? Si hay pocos datos, dilo. Corto.`}],sys,500)); }
    catch(e){ setTrend(aiErr()); } setBusy(false); };
  return (
    <div className="pop">
      {/* objetivo */}
      <div style={{background:C.panel,border:`1px solid ${C.line}`,borderRadius:16,padding:"16px 18px",marginBottom:12}}>
        <div style={{display:"flex",justifyContent:"space-between",alignItems:"flex-end",marginBottom:10}}>
          <div><div style={{fontSize:11,color:C.muted,fontWeight:700,letterSpacing:".1em",textTransform:"uppercase"}}>Peso actual</div><div className="disp" style={{fontSize:40,marginTop:2}}>{lastW} <span style={{fontSize:16,color:C.muted}}>kg</span></div></div>
          <div style={{textAlign:"right",display:"flex",alignItems:"center",gap:6,color:C.lime,fontWeight:800,fontSize:15}}><Target size={16}/>meta {GOAL_W} kg</div>
        </div>
        <div style={{height:9,background:C.panel2,borderRadius:6,overflow:"hidden"}}><div style={{height:"100%",width:goalPct+"%",background:`linear-gradient(90deg,${C.cyan},${C.lime})`,borderRadius:6,transition:"width .6s"}}/></div>
        <div style={{display:"flex",justifyContent:"space-between",fontSize:11,color:C.muted,marginTop:5}}><span>{startW} kg inicio</span><span>{toGoal>0?`faltan ${toGoal.toFixed(1)} kg`:"¡meta alcanzada!"}</span></div>
      </div>

      {chartW.length>=2 && (<div style={{background:C.panel,border:`1px solid ${C.line}`,borderRadius:16,padding:"12px 16px 6px",marginBottom:12}}><div style={{fontSize:12.5,fontWeight:800,marginBottom:2}}>Tendencia de peso</div><Chart entries={chartW} color={C.cyan} height={140}/></div>)}

      {weights.length>0 && (<><button onClick={analyze} disabled={busy} style={{width:"100%",padding:"11px",borderRadius:12,border:`1px solid ${C.line}`,cursor:"pointer",background:C.panel,color:C.lime,fontWeight:800,fontSize:13.5,display:"flex",alignItems:"center",justifyContent:"center",gap:8,marginBottom:4}}>{busy?<><Loader2 size={15} style={{animation:"spin 1s linear infinite"}}/>Analizando…</>:<><LineChart size={16}/>Analizar tendencia con IA</>}</button><AIPanel title="Análisis de tendencia" busy={busy} text={trend} color={C.cyan}/></>)}

      <div style={{background:C.panel,border:`1px solid ${C.line}`,borderRadius:16,padding:14,margin:"16px 0 18px"}}>
        <div style={{display:"flex",gap:6,marginBottom:10,flexWrap:"wrap"}}>{Object.keys(TYPES).map(k=>(<button key={k} onClick={()=>setType(k)} style={{padding:"6px 11px",borderRadius:999,fontSize:11.5,fontWeight:700,cursor:"pointer",border:`1px solid ${type===k?TYPES[k][1]:C.line}`,background:type===k?"rgba(255,255,255,.05)":"transparent",color:type===k?TYPES[k][1]:C.muted}}>{TYPES[k][0]}</button>))}</div>
        {type==="peso"?(<div style={{display:"flex",alignItems:"center",gap:8}}><Scale size={18} color={C.cyan}/><input value={weight} onChange={e=>setWeight(e.target.value)} type="number" inputMode="decimal" className="ph" placeholder="93.9" style={{flex:1,background:C.panel2,border:`1px solid ${C.line}`,borderRadius:10,padding:"10px 12px",color:C.ink,fontSize:14,outline:"none"}}/><span style={{color:C.muted,fontSize:14}}>kg</span></div>)
        :(<textarea value={text} onChange={e=>setText(e.target.value)} rows={2} className="ph" placeholder={type==="entreno"?"Subí el peso muerto a 125 kg x5…":type==="sensacion"?"Energía alta, dormí bien…":"Lo que quieras anotar…"} style={{width:"100%",resize:"none",background:C.panel2,border:`1px solid ${C.line}`,borderRadius:10,padding:"10px 12px",color:C.ink,fontSize:13.5,outline:"none"}}/>)}
        <button onClick={add} style={{width:"100%",marginTop:8,padding:"10px",borderRadius:10,border:"none",cursor:"pointer",background:C.lime,color:"#1a2400",fontWeight:800,fontSize:14}}>Guardar</button>
      </div>
      {notes.length===0 && <div style={{color:C.muted,fontSize:13,textAlign:"center",padding:"16px 0"}}>Tu bitácora está vacía.</div>}
      {notes.map(n=>{ const col=(TYPES[n.type]||["",C.muted])[1]; const d=new Date(n.date);
        return (<div key={n.id} className="pop" style={{background:C.panel,border:`1px solid ${C.line}`,borderRadius:13,padding:"11px 14px",marginBottom:9,display:"flex",gap:10,alignItems:"flex-start"}}>
          <div style={{flex:1}}><div style={{display:"flex",alignItems:"center",gap:8,marginBottom:3}}><span style={{fontSize:10,fontWeight:800,letterSpacing:".08em",textTransform:"uppercase",color:col}}>{(TYPES[n.type]||["Nota"])[0]}</span><span style={{fontSize:11,color:C.muted}}>{fdate(n.date)} · {d.toLocaleTimeString("es",{hour:"2-digit",minute:"2-digit"})}</span></div><div style={{fontSize:13.5}}>{n.text}</div></div>
          <button onClick={()=>del(n.id)} style={{background:"none",border:"none",cursor:"pointer",color:C.muted}}><Trash2 size={16}/></button></div>);
      })}
    </div>
  );
}

/* ===================== PLAN ===================== */
function Plan({presetKey}){
  const [openSlot,setOpenSlot]=useState("Cena");
  const [shopBusy,setShopBusy]=useState(false); const [shop,setShop]=useState("");
  const macros={ definicion:[220,265,70], mantenimiento:[200,360,85], volumen:[200,450,90] };
  const genShop=async()=>{ setShopBusy(true); setShop("");
    try{ const sys=`Eres nutricionista. ${PROFILE} Plan hiperproteico de definición ~2600 kcal, 220 g proteína/día. Español, conciso.`;
      setShop(await callClaude([{role:"user",content:"Genera una lista de compras semanal para 1 persona (7 días) acorde a este plan: agrupa por categorías (Proteínas, Carbohidratos, Verduras y frutas, Grasas, Básicos/suplementos) con cantidades aproximadas. Breve."}],sys,700)); }
    catch(e){ setShop(aiErr()); } setShopBusy(false);
  };
  return (
    <div className="pop">
      <div className="disp" style={{fontSize:24,color:C.lime,marginBottom:4}}>PAUTA NUTRICIONAL</div>
      <p style={{fontSize:12.5,color:C.muted,marginBottom:14}}>Definición hiperproteica · basal medido 1.866 kcal · recomponer hacia ~85 kg manteniendo músculo.</p>
      <div style={{display:"flex",gap:8,marginBottom:16}}>
        {Object.keys(PRESETS).map(k=>{ const m=macros[k]; const a=k===presetKey;
          return (<div key={k} style={{flex:1,background:a?"rgba(205,255,74,.08)":C.panel,border:`1px solid ${a?C.lime:C.line}`,borderRadius:13,padding:"12px 10px"}}>
            <div style={{fontSize:10.5,fontWeight:800,textTransform:"uppercase",color:a?C.lime:C.muted}}>{PRESETS[k].label}</div>
            <div className="disp" style={{fontSize:22,margin:"3px 0"}}>{PRESETS[k].kcal}</div>
            <div style={{fontSize:11,color:C.muted,lineHeight:1.5}}><span style={{color:C.cyan}}>P {m[0]}</span> · C {m[1]} · <span style={{color:C.amber}}>G {m[2]}</span></div>
          </div>); })}
      </div>
      <div style={{fontSize:13,fontWeight:800,marginBottom:8}}>Opciones por comida</div>
      {MEALS.map(meal=>{ const o=openSlot===meal.slot;
        return (<div key={meal.slot} style={{background:C.panel,border:`1px solid ${o?C.lime:C.line}`,borderRadius:13,marginBottom:9,overflow:"hidden"}}>
          <button onClick={()=>setOpenSlot(o?null:meal.slot)} style={{width:"100%",background:"none",border:"none",cursor:"pointer",padding:"12px 14px",display:"flex",alignItems:"center",gap:10,color:C.ink}}>
            <span style={{flex:1,textAlign:"left",fontSize:14,fontWeight:700}}>{meal.slot}</span><span style={{fontSize:11.5,color:C.muted}}>{meal.kcal} kcal</span><span style={{color:C.muted}}>{o?"▴":"▾"}</span>
          </button>
          {o && (<div className="pop" style={{padding:"0 14px 12px"}}>{meal.opts.map((op,i)=>(<div key={i} style={{display:"flex",gap:9,padding:"8px 0",borderTop:`1px solid ${C.line}`}}><span style={{fontFamily:"'Bebas Neue'",color:C.lime,fontSize:15,minWidth:16}}>{String.fromCharCode(65+i)}</span><span style={{fontSize:13,color:"#dcdfce"}}>{op}</span></div>))}</div>)}
        </div>);
      })}

      <button onClick={genShop} disabled={shopBusy} style={{width:"100%",marginTop:8,padding:"11px",borderRadius:12,border:`1px solid ${C.line}`,cursor:"pointer",background:C.panel,color:C.lime,fontWeight:800,fontSize:13.5,display:"flex",alignItems:"center",justifyContent:"center",gap:8}}>{shopBusy?<><Loader2 size={15} style={{animation:"spin 1s linear infinite"}}/>Generando…</>:<><ShoppingCart size={16}/>Generar lista de compras (IA)</>}</button>
      <AIPanel title="Lista de compras semanal" busy={shopBusy} text={shop}/>

      <div style={{fontSize:13,fontWeight:800,margin:"16px 0 8px"}}>Pautas clave</div>
      <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:9}}>
        {PAUTAS.map(([t,d])=>(<div key={t} style={{background:C.panel,border:`1px solid ${C.line}`,borderRadius:12,padding:"11px 13px"}}><div style={{fontSize:12.5,fontWeight:700,marginBottom:3}}>{t}</div><div style={{fontSize:11.5,color:C.muted,lineHeight:1.45}}>{d}</div></div>))}
      </div>
      <div style={{fontSize:11,color:C.muted,marginTop:16,textAlign:"center",lineHeight:1.5}}>Orientación de nutrición deportiva, no prescripción médica. Las estimaciones de IA son aproximadas.</div>
    </div>
  );
}
