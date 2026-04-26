import React, { useState } from "react";

const PACKS = {
  ghana: { name: "Ghana", signal1: "Informality rate: 78%", signal2: "Wage-salaried share: 32%" },
  kenya: { name: "Kenya", signal1: "Informality rate: 73%", signal2: "Wage-salaried share: 29%" },
};

export default function App() {
  const [country, setCountry] = useState("ghana");
  const [educationLevel, setEducationLevel] = useState("Secondary School Certificate");
  const [informalWorkHistory, setInformalWorkHistory] = useState("Runs a phone repair business and taught herself basic coding from YouTube.");
  const [languages, setLanguages] = useState("English, Twi, Hausa");
  const [tasks, setTasks] = useState("Repair phones, talk to customers, basic diagnostics, post on WhatsApp");
  const [result, setResult] = useState(null);

  const submit = async () => {
    const payload = { country, education_level: educationLevel, informal_work_history: informalWorkHistory, languages: languages.split(",").map(s => s.trim()), tasks: tasks.split(",").map(s => s.trim()) };
    const [a, r, m] = await Promise.all([
      fetch("/analyze-profile", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) }).then(x => x.json()),
      fetch("/risk-score", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) }).then(x => x.json()),
      fetch("/match-opportunities", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) }).then(x => x.json()),
    ]);
    setResult({ analyze: a, risk: r, match: m });
  };

  return <div style={{fontFamily:'Inter, sans-serif', background:'#f7f8fb', minHeight:'100vh'}}>
    <header style={{background:'#0f172a', color:'#fff', padding:'20px 32px'}}>
      <div style={{maxWidth:1200, margin:'0 auto', display:'flex', justifyContent:'space-between', alignItems:'center', gap:16, flexWrap:'wrap'}}>
        <div>
          <h1 style={{margin:0}}>UNMAPPED</h1>
          <p style={{margin:'6px 0 0', opacity:0.85}}>Open infrastructure for skills-to-opportunity matching</p>
        </div>
        <div style={{display:'flex', gap:12, alignItems:'center'}}>
          <label style={{fontSize:14}}>Country</label>
          <select value={country} onChange={e=>setCountry(e.target.value)} style={{padding:'10px 12px', borderRadius:10, border:'1px solid #334155'}}>
            {Object.keys(PACKS).map(k=><option key={k} value={k}>{PACKS[k].name}</option>)}
          </select>
        </div>
      </div>
    </header>

    <main style={{maxWidth:1200, margin:'0 auto', padding:'28px 32px'}}>
      <div style={{display:'grid', gridTemplateColumns:'1.1fr 0.9fr', gap:24, alignItems:'start'}}>
        <section style={{background:'#fff', padding:24, borderRadius:16, boxShadow:'0 8px 30px rgba(15,23,42,0.08)'}}>
          <h2 style={{marginTop:0}}>Profile input</h2>
          <div style={{display:'grid', gap:12}}>
            <input value={educationLevel} onChange={e=>setEducationLevel(e.target.value)} placeholder="Education level" style={inputStyle} />
            <textarea value={informalWorkHistory} onChange={e=>setInformalWorkHistory(e.target.value)} rows={4} style={inputStyle} />
            <input value={languages} onChange={e=>setLanguages(e.target.value)} placeholder="Languages" style={inputStyle} />
            <input value={tasks} onChange={e=>setTasks(e.target.value)} placeholder="Tasks" style={inputStyle} />
            <button onClick={submit} style={buttonStyle}>Analyze profile</button>
          </div>
        </section>

        <aside style={{display:'grid', gap:24}}>
          <Card title="Design goals" items={[
            'Human-readable skills profile',
            'Explainable risk lens',
            'Realistic opportunity fit',
            'Country-switchable config',
          ]} />
          <Card title="Country signals" items={[PACKS[country].signal1, PACKS[country].signal2]} />
        </aside>
      </div>

      {result && <div style={{display:'grid', gridTemplateColumns:'1fr', gap:20, marginTop:24}}>
        <section style={panelStyle}>
          <h2>Skills translation output</h2>
          <p><b>Portable profile:</b></p>
          <p>Education: {result.analyze.portable_profile.education}</p>
          <p>Skills: {result.analyze.portable_profile.skills.join(', ')}</p>
          <p>Languages: {result.analyze.portable_profile.languages.join(', ')}</p>
          <p><b>Why this fits:</b> {result.analyze.why_this_fits}</p>
        </section>

        <section style={panelStyle}>
          <h2>AI readiness panel</h2>
          <p><b>Automation risk:</b> {result.risk.automation_risk}/100</p>
          <div style={{height:12, background:'#e5e7eb', borderRadius:999, overflow:'hidden', marginBottom:12}}>
            <div style={{width:`${result.risk.automation_risk}%`, height:'100%', background:'linear-gradient(90deg, #f59e0b, #ef4444)'}} />
          </div>
          <p><b>Durable skills:</b> {result.risk.durable_skills.join(', ')}</p>
          <p><b>Exposed tasks:</b> {result.risk.exposed_tasks.join(', ')}</p>
        </section>

        <section style={panelStyle}>
          <h2>Opportunity matches</h2>
          <div style={{display:'grid', gap:12}}>
            {result.match.matches.map((x,i)=><div key={i} style={{padding:16, border:'1px solid #e5e7eb', borderRadius:14, background:'#fafafa'}}>
              <div style={{display:'flex', justifyContent:'space-between', gap:12, flexWrap:'wrap'}}>
                <b>{x.title}</b><span>{x.fit}% fit</span>
              </div>
              <div style={{color:'#475569', marginTop:6}}>{x.type}</div>
            </div>)}
          </div>
          <p style={{marginTop:16}}><b>Why these matches:</b> They use the skills already present in the profile and keep the pathway realistic.</p>
        </section>
      </div>}
    </main>
  </div>
}

function Card({ title, items }) {
  return <div style={panelStyle}>
    <h3 style={{marginTop:0}}>{title}</h3>
    <ul style={{margin:0, paddingLeft:18, color:'#334155'}}>
      {items.map((x,i)=><li key={i} style={{marginBottom:8}}>{x}</li>)}
    </ul>
  </div>
}

const inputStyle = {padding:'12px 14px', border:'1px solid #cbd5e1', borderRadius:12, fontSize:16, width:'100%', boxSizing:'border-box', background:'#fff'};
const buttonStyle = {padding:'12px 16px', border:'none', borderRadius:12, background:'#2563eb', color:'#fff', fontWeight:600, cursor:'pointer', width:'fit-content'};
const panelStyle = {background:'#fff', padding:24, borderRadius:16, boxShadow:'0 8px 30px rgba(15,23,42,0.08)'};
