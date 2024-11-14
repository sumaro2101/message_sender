import{a as D,b as L}from"./chunk-P2VM2T3G.js";var T=D((U,d)=>{(function(A){let u;function f(a,e){let i=a.charCodeAt(e);if(isNaN(i))throw new RangeError("Index "+e+' out of range for string "'+a+'"; please open an issue at https://github.com/Trott/slug/issues/new');if(i<55296||i>57343)return[a.charAt(e),e];if(i>=55296&&i<=56319){if(a.length<=e+1)return[" ",e];let n=a.charCodeAt(e+1);return n<56320||n>57343?[" ",e]:[a.charAt(e)+a.charAt(e+1),e+1]}if(e===0)return[" ",e];let c=a.charCodeAt(e-1);if(c<55296||c>56319)return[" ",e];throw new Error('String "'+a+'" reaches code believed to be unreachable; please open an issue at https://github.com/Trott/slug/issues/new')}typeof window<"u"?window.btoa?u=function(a){return btoa(unescape(encodeURIComponent(a)))}:u=function(a){let e=unescape(encodeURIComponent(a+"")),i="";for(let c,n,h=0,s="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";e.charAt(h|0)||(s="=",h%1);i+=s.charAt(63&c>>8-h%1*8)){if(n=e.charCodeAt(h+=3/4),n>255)throw new Error("'btoa' failed: The string to be encoded contains characters outside of the Latin1 range.");c=c<<8|n}return i}:u=function(a){return Buffer.from(a).toString("base64")};function t(a,e){let i=b(a,e);if((e&&e.fallback!==void 0?e.fallback:t.defaults.fallback)===!0&&i===""){let n="";for(let h=0;h<a.length;h++){let s=f(a,h);h=s[1],n+=s[0]}i=b(u(n),e)}return i}let m={bg:{\u0419:"Y",\u0439:"y",X:"H",x:"h",\u0426:"Ts",\u0446:"ts",\u0429:"Sht",\u0449:"sht",\u042A:"A",\u044A:"a",\u042C:"Y",\u044C:"y"},de:{\u00C4:"AE",\u00E4:"ae",\u00D6:"OE",\u00F6:"oe",\u00DC:"UE",\u00FC:"ue"},sr:{\u0111:"dj",\u0110:"DJ"},uk:{\u0418:"Y",\u0438:"y",\u0419:"Y",\u0439:"y",\u0426:"Ts",\u0446:"ts",\u0425:"Kh",\u0445:"kh",\u0429:"Shch",\u0449:"shch",\u0413:"H",\u0433:"h"}},p={};function b(a,e){if(typeof a!="string")throw new Error("slug() requires a string argument, received "+typeof a);typeof e=="string"&&(e={replacement:e}),e=e?Object.assign({},e):{},e.mode=e.mode||t.defaults.mode;let i=t.defaults.modes[e.mode],c=["replacement","multicharmap","charmap","remove","lower","trim"];for(let r,l=0,g=c.length;l<g;l++)r=c[l],e[r]=r in e?e[r]:i[r];let n=m[e.locale]||p,h=[];for(let r in e.multicharmap){if(!Object.prototype.hasOwnProperty.call(e.multicharmap,r))continue;let l=r.length;h.indexOf(l)===-1&&h.push(l)}h=h.sort(function(r,l){return l-r});let s=e.mode==="rfc3986"?/[^\w\s\-.~]/:/[^A-Za-z0-9\s]/,o="";for(let r,l=0,g=a.length;l<g;l++){r=a[l];let k=!1;for(let E=0;E<h.length;E++){let w=h[E],I=a.substr(l,w);if(e.multicharmap[I]){l+=w-1,r=e.multicharmap[I],k=!0;break}}k||(n[r]?r=n[r]:e.charmap[r]?r=e.charmap[r].replace(e.replacement," "):r.includes(e.replacement)?r=r.replace(e.replacement," "):r=r.replace(s,"")),o+=r}return e.remove&&(o=o.replace(e.remove,"")),e.trim&&(o=o.trim()),o=o.replace(/\s+/g,e.replacement),e.lower&&(o=o.toLowerCase()),o}let y={\u092B\u093C:"Fi",\u0917\u093C:"Ghi",\u0916\u093C:"Khi",\u0915\u093C:"Qi",\u0921\u093C:"ugDha",\u0922\u093C:"ugDhha",\u092F\u093C:"Yi",\u091C\u093C:"Za",\u05D1\u05B4\u05D9:"i",\u05D1\u05B5:"e",\u05D1\u05B5\u05D9:"e",\u05D1\u05B6:"e",\u05D1\u05B7:"a",\u05D1\u05B8:"a",\u05D1\u05B9:"o",\u05D5\u05B9:"o",\u05D1\u05BB:"u",\u05D5\u05BC:"u",\u05D1\u05BC:"b",\u05DB\u05BC:"k",\u05DA\u05BC:"k",\u05E4\u05BC:"p",\u05E9\u05C1:"sh",\u05E9\u05C2:"s",\u05D1\u05B0:"e",\u05D7\u05B1:"e",\u05D7\u05B2:"a",\u05D7\u05B3:"o",\u05D1\u05B4:"i"},O={\u00C0:"A",\u00C1:"A",\u00C2:"A",\u00C3:"A",\u00C4:"A",\u00C5:"A",\u00C6:"AE",\u00C7:"C",\u00C8:"E",\u00C9:"E",\u00CA:"E",\u00CB:"E",\u00CC:"I",\u00CD:"I",\u00CE:"I",\u00CF:"I",\u00D0:"D",\u00D1:"N",\u00D2:"O",\u00D3:"O",\u00D4:"O",\u00D5:"O",\u00D6:"O",\u0150:"O",\u00D8:"O",\u014C:"O",\u00D9:"U",\u00DA:"U",\u00DB:"U",\u00DC:"U",\u0170:"U",\u00DD:"Y",\u00DE:"TH",\u00DF:"ss",\u00E0:"a",\u00E1:"a",\u00E2:"a",\u00E3:"a",\u00E4:"a",\u00E5:"a",\u00E6:"ae",\u00E7:"c",\u00E8:"e",\u00E9:"e",\u00EA:"e",\u00EB:"e",\u00EC:"i",\u00ED:"i",\u00EE:"i",\u00EF:"i",\u00F0:"d",\u00F1:"n",\u00F2:"o",\u00F3:"o",\u00F4:"o",\u00F5:"o",\u00F6:"o",\u0151:"o",\u00F8:"o",\u014D:"o",\u0152:"OE",\u0153:"oe",\u00F9:"u",\u00FA:"u",\u00FB:"u",\u00FC:"u",\u0171:"u",\u00FD:"y",\u00FE:"th",\u00FF:"y","\u1E9E":"SS",\u03B1:"a",\u03B2:"b",\u03B3:"g",\u03B4:"d",\u03B5:"e",\u03B6:"z",\u03B7:"h",\u03B8:"th",\u03B9:"i",\u03BA:"k",\u03BB:"l",\u03BC:"m",\u03BD:"n",\u03BE:"3",\u03BF:"o",\u03C0:"p",\u03C1:"r",\u03C3:"s",\u03C4:"t",\u03C5:"y",\u03C6:"f",\u03C7:"x",\u03C8:"ps",\u03C9:"w",\u03AC:"a",\u03AD:"e",\u03AF:"i",\u03CC:"o",\u03CD:"y",\u03AE:"h",\u03CE:"w",\u03C2:"s",\u03CA:"i",\u03B0:"y",\u03CB:"y",\u0390:"i",\u0391:"A",\u0392:"B",\u0393:"G",\u0394:"D",\u0395:"E",\u0396:"Z",\u0397:"H",\u0398:"Th",\u0399:"I",\u039A:"K",\u039B:"L",\u039C:"M",\u039D:"N",\u039E:"3",\u039F:"O",\u03A0:"P",\u03A1:"R",\u03A3:"S",\u03A4:"T",\u03A5:"Y",\u03A6:"F",\u03A7:"X",\u03A8:"PS",\u03A9:"W",\u0386:"A",\u0388:"E",\u038A:"I",\u038C:"O",\u038E:"Y",\u0389:"H",\u038F:"W",\u03AA:"I",\u03AB:"Y",\u015F:"s",\u015E:"S",\u0131:"i",\u0130:"I",\u011F:"g",\u011E:"G",\u0430:"a",\u0431:"b",\u0432:"v",\u0433:"g",\u0434:"d",\u0435:"e",\u0451:"yo",\u0436:"zh",\u0437:"z",\u0438:"i",\u0439:"j",\u043A:"k",\u043B:"l",\u043C:"m",\u043D:"n",\u043E:"o",\u043F:"p",\u0440:"r",\u0441:"s",\u0442:"t",\u0443:"u",\u0444:"f",\u0445:"h",\u0446:"c",\u0447:"ch",\u0448:"sh",\u0449:"sh",\u044A:"u",\u044B:"y",\u044C:"",\u044D:"e",\u044E:"yu",\u044F:"ya",\u0410:"A",\u0411:"B",\u0412:"V",\u0413:"G",\u0414:"D",\u0415:"E",\u0401:"Yo",\u0416:"Zh",\u0417:"Z",\u0418:"I",\u0419:"J",\u041A:"K",\u041B:"L",\u041C:"M",\u041D:"N",\u041E:"O",\u041F:"P",\u0420:"R",\u0421:"S",\u0422:"T",\u0423:"U",\u0424:"F",\u0425:"H",\u0426:"C",\u0427:"Ch",\u0428:"Sh",\u0429:"Sh",\u042A:"U",\u042B:"Y",\u042C:"",\u042D:"E",\u042E:"Yu",\u042F:"Ya",\u0404:"Ye",\u0406:"I",\u0407:"Yi",\u0490:"G",\u0454:"ye",\u0456:"i",\u0457:"yi",\u0491:"g",\u010D:"c",\u010F:"d",\u011B:"e",\u0148:"n",\u0159:"r",\u0161:"s",\u0165:"t",\u016F:"u",\u017E:"z",\u010C:"C",\u010E:"D",\u011A:"E",\u0147:"N",\u0158:"R",\u0160:"S",\u0164:"T",\u016E:"U",\u017D:"Z",\u013E:"l",\u013A:"l",\u0155:"r",\u013D:"L",\u0139:"L",\u0154:"R",\u0105:"a",\u0107:"c",\u0119:"e",\u0142:"l",\u0144:"n",\u015B:"s",\u017A:"z",\u017C:"z",\u0104:"A",\u0106:"C",\u0118:"E",\u0141:"L",\u0143:"N",\u015A:"S",\u0179:"Z",\u017B:"Z",\u0101:"a",\u0113:"e",\u0123:"g",\u012B:"i",\u0137:"k",\u013C:"l",\u0146:"n",\u016B:"u",\u0100:"A",\u0112:"E",\u0122:"G",\u012A:"I",\u0136:"K",\u013B:"L",\u0145:"N",\u016A:"U",\u0623:"a",\u0625:"i",\u0628:"b",\u062A:"t",\u062B:"th",\u062C:"g",\u062D:"h",\u062E:"kh",\u062F:"d",\u0630:"th",\u0631:"r",\u0632:"z",\u0633:"s",\u0634:"sh",\u0635:"s",\u0636:"d",\u0637:"t",\u0638:"th",\u0639:"aa",\u063A:"gh",\u0641:"f",\u0642:"k",\u0643:"k",\u0644:"l",\u0645:"m",\u0646:"n",\u0647:"h",\u0648:"o",\u064A:"y",\u0621:"aa",\u0629:"a",\u0622:"a",\u0627:"a",\u067E:"p",\u0698:"zh",\u06AF:"g",\u0686:"ch",\u06A9:"k",\u06CC:"i",\u0117:"e",\u012F:"i",\u0173:"u",\u0116:"E",\u012E:"I",\u0172:"U",\u021B:"t",\u021A:"T",\u0163:"t",\u0162:"T",\u0219:"s",\u0218:"S",\u0103:"a",\u0102:"A",\u1EA0:"A",\u1EA2:"A",\u1EA6:"A",\u1EA4:"A",\u1EAC:"A",\u1EA8:"A",\u1EAA:"A",\u1EB0:"A",\u1EAE:"A",\u1EB6:"A",\u1EB2:"A",\u1EB4:"A",\u1EB8:"E",\u1EBA:"E",\u1EBC:"E",\u1EC0:"E",\u1EBE:"E",\u1EC6:"E",\u1EC2:"E",\u1EC4:"E",\u1ECA:"I",\u1EC8:"I",\u0128:"I",\u1ECC:"O",\u1ECE:"O",\u1ED2:"O",\u1ED0:"O",\u1ED8:"O",\u1ED4:"O",\u1ED6:"O",\u01A0:"O",\u1EDC:"O",\u1EDA:"O",\u1EE2:"O",\u1EDE:"O",\u1EE0:"O",\u1EE4:"U",\u1EE6:"U",\u0168:"U",\u01AF:"U",\u1EEA:"U",\u1EE8:"U",\u1EF0:"U",\u1EEC:"U",\u1EEE:"U",\u1EF2:"Y",\u1EF4:"Y",\u1EF6:"Y",\u1EF8:"Y",\u0110:"D",\u1EA1:"a",\u1EA3:"a",\u1EA7:"a",\u1EA5:"a",\u1EAD:"a",\u1EA9:"a",\u1EAB:"a",\u1EB1:"a",\u1EAF:"a",\u1EB7:"a",\u1EB3:"a",\u1EB5:"a",\u1EB9:"e",\u1EBB:"e",\u1EBD:"e",\u1EC1:"e",\u1EBF:"e",\u1EC7:"e",\u1EC3:"e",\u1EC5:"e",\u1ECB:"i",\u1EC9:"i",\u0129:"i",\u1ECD:"o",\u1ECF:"o",\u1ED3:"o",\u1ED1:"o",\u1ED9:"o",\u1ED5:"o",\u1ED7:"o",\u01A1:"o",\u1EDD:"o",\u1EDB:"o",\u1EE3:"o",\u1EDF:"o",\u1EE1:"o",\u1EE5:"u",\u1EE7:"u",\u0169:"u",\u01B0:"u",\u1EEB:"u",\u1EE9:"u",\u1EF1:"u",\u1EED:"u",\u1EEF:"u",\u1EF3:"y",\u1EF5:"y",\u1EF7:"y",\u1EF9:"y",\u0111:"d",\u04D8:"AE",\u04D9:"ae",\u0492:"GH",\u0493:"gh",\u049A:"KH",\u049B:"kh",\u04A2:"NG",\u04A3:"ng",\u04AE:"UE",\u04AF:"ue",\u04B0:"U",\u04B1:"u",\u04BA:"H",\u04BB:"h",\u04E8:"OE",\u04E9:"oe",\u0452:"dj",\u0458:"j",\u0459:"lj",\u045A:"nj",\u045B:"c",\u045F:"dz",\u0402:"Dj",\u0408:"j",\u0409:"Lj",\u040A:"Nj",\u040B:"C",\u040F:"Dz",\u01CC:"nj",\u01C9:"lj",\u01CB:"NJ",\u01C8:"LJ",\u0905:"a",\u0906:"aa",\u090F:"e",\u0908:"ii",\u090D:"ei",\u090E:"ae",\u0910:"ai",\u0907:"i",\u0913:"o",\u0911:"oi",\u0912:"oii",\u090A:"uu",\u0914:"ou",\u0909:"u",\u092C:"B",\u092D:"Bha",\u091A:"Ca",\u091B:"Chha",\u0921:"Da",\u0922:"Dha",\u092B:"Fa",\u0917:"Ga",\u0918:"Gha",\u0917\u093C:"Ghi",\u0939:"Ha",\u091C:"Ja",\u091D:"Jha",\u0915:"Ka",\u0916:"Kha",\u0916\u093C:"Khi",\u0932:"L",\u0933:"Li",\u090C:"Li",\u0934:"Lii",\u0961:"Lii",\u092E:"Ma",\u0928:"Na",\u0919:"Na",\u091E:"Nia",\u0923:"Nae",\u0929:"Ni",\u0950:"oms",\u092A:"Pa",\u0915\u093C:"Qi",\u0930:"Ra",\u090B:"Ri",\u0960:"Ri",\u0931:"Ri",\u0938:"Sa",\u0936:"Sha",\u0937:"Shha",\u091F:"Ta",\u0924:"Ta",\u0920:"Tha",\u0926:"Tha",\u0925:"Tha",\u0927:"Thha",\u0921\u093C:"ugDha",\u0922\u093C:"ugDhha",\u0935:"Va",\u092F:"Ya",\u092F\u093C:"Yi",\u091C\u093C:"Za",\u0259:"e",\u018F:"E",\u10D0:"a",\u10D1:"b",\u10D2:"g",\u10D3:"d",\u10D4:"e",\u10D5:"v",\u10D6:"z",\u10D7:"t",\u10D8:"i",\u10D9:"k",\u10DA:"l",\u10DB:"m",\u10DC:"n",\u10DD:"o",\u10DE:"p",\u10DF:"zh",\u10E0:"r",\u10E1:"s",\u10E2:"t",\u10E3:"u",\u10E4:"p",\u10E5:"k",\u10E6:"gh",\u10E7:"q",\u10E8:"sh",\u10E9:"ch",\u10EA:"ts",\u10EB:"dz",\u10EC:"ts",\u10ED:"ch",\u10EE:"kh",\u10EF:"j",\u10F0:"h",\u05D1:"v",\u05D2\u05BC:"g",\u05D2:"g",\u05D3:"d",\u05D3\u05BC:"d",\u05D4:"h",\u05D5:"v",\u05D6:"z",\u05D7:"h",\u05D8:"t",\u05D9:"y",\u05DB:"kh",\u05DA:"kh",\u05DC:"l",\u05DE:"m",\u05DD:"m",\u05E0:"n",\u05DF:"n",\u05E1:"s",\u05E4:"f",\u05E3:"f",\u05E5:"ts",\u05E6:"ts",\u05E7:"k",\u05E8:"r",\u05EA\u05BC:"t",\u05EA:"t"};t.charmap=Object.assign({},O),t.multicharmap=Object.assign({},y),t.defaults={charmap:t.charmap,mode:"pretty",modes:{rfc3986:{replacement:"-",remove:null,lower:!0,charmap:t.charmap,multicharmap:t.multicharmap,trim:!0},pretty:{replacement:"-",remove:null,lower:!0,charmap:t.charmap,multicharmap:t.multicharmap,trim:!0}},multicharmap:t.multicharmap,fallback:!0},t.reset=function(){t.defaults.modes.rfc3986.charmap=t.defaults.modes.pretty.charmap=t.charmap=t.defaults.charmap=Object.assign({},O),t.defaults.modes.rfc3986.multicharmap=t.defaults.modes.pretty.multicharmap=t.multicharmap=t.defaults.multicharmap=Object.assign({},y),p=""},t.extend=function(a){let e=Object.keys(a),i={},c={};for(let n=0;n<e.length;n++)e[n].length>1?i[e[n]]=a[e[n]]:c[e[n]]=a[e[n]];Object.assign(t.charmap,c),Object.assign(t.multicharmap,i)},t.setLocale=function(a){p=m[a]||{}},typeof d<"u"&&d.exports?d.exports=t:A.slug=t})(U)});var C=L(T()),j=class extends HTMLInputElement{connectedCallback(){var t;let u=this.getAttribute("populate-from");if(!u)throw new Error(`Element ${this} requires an attribute populate-from="...".`);let f=(t=this.form)==null?void 0:t.elements.namedItem(u);if(!(f instanceof HTMLInputElement))throw new Error(`Element <input name="${u}"> is missing on this form.`);this.value===""&&f.addEventListener("input",m=>{m.currentTarget instanceof HTMLInputElement&&(this.value=(0,C.default)(m.currentTarget.value),this.dispatchEvent(new Event("input")))})}};export{j as DjangoSlugElement};
