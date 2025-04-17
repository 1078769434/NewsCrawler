var $e = {
    wbiImgKey: 'c6618eced9b64a019d0e6247aed7a38e',
    wbiSubKey: '6bb3adc89c244ccda6d9abf22fc6f910'
};

var localStorage = function() {}
localStorage.wbi_img_url = 'https://i0.hdslb.com/bfs/wbi/980bc31dc6124ac2b21b5fd63e419279.png';
localStorage.wbi_sub_url = 'https://i0.hdslb.com/bfs/wbi/497ed2ee3fe5455f82bb6b4af9cd9584.png';
localStorage.getItem = function(keys) {
    return localStorage[keys];
}

function createCommonjsModule(pe, $e) {
    return $e = {
        exports: {}
    },
    pe($e, $e.exports),
    $e.exports
}

var crypt = createCommonjsModule(function(pe) {
    (function() {
        var $e = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
          , Pe = {
            rotl: function(Me, Fe) {
                return Me << Fe | Me >>> 32 - Fe
            },
            rotr: function(Me, Fe) {
                return Me << 32 - Fe | Me >>> Fe
            },
            endian: function(Me) {
                if (Me.constructor == Number)
                    return Pe.rotl(Me, 8) & 16711935 | Pe.rotl(Me, 24) & 4278255360;
                for (var Fe = 0; Fe < Me.length; Fe++)
                    Me[Fe] = Pe.endian(Me[Fe]);
                return Me
            },
            randomBytes: function(Me) {
                for (var Fe = []; Me > 0; Me--)
                    Fe.push(Math.floor(Math.random() * 256));
                return Fe
            },
            bytesToWords: function(Me) {
                for (var Fe = [], Le = 0, je = 0; Le < Me.length; Le++,
                je += 8)
                    Fe[je >>> 5] |= Me[Le] << 24 - je % 32;
                return Fe
            },
            wordsToBytes: function(Me) {
                for (var Fe = [], Le = 0; Le < Me.length * 32; Le += 8)
                    Fe.push(Me[Le >>> 5] >>> 24 - Le % 32 & 255);
                return Fe
            },
            bytesToHex: function(Me) {
                for (var Fe = [], Le = 0; Le < Me.length; Le++)
                    Fe.push((Me[Le] >>> 4).toString(16)),
                    Fe.push((Me[Le] & 15).toString(16));
                return Fe.join("")
            },
            hexToBytes: function(Me) {
                for (var Fe = [], Le = 0; Le < Me.length; Le += 2)
                    Fe.push(parseInt(Me.substr(Le, 2), 16));
                return Fe
            },
            bytesToBase64: function(Me) {
                for (var Fe = [], Le = 0; Le < Me.length; Le += 3)
                    for (var je = Me[Le] << 16 | Me[Le + 1] << 8 | Me[Le + 2], Be = 0; Be < 4; Be++)
                        Le * 8 + Be * 6 <= Me.length * 8 ? Fe.push($e.charAt(je >>> 6 * (3 - Be) & 63)) : Fe.push("=");
                return Fe.join("")
            },
            base64ToBytes: function(Me) {
                Me = Me.replace(/[^A-Z0-9+\/]/ig, "");
                for (var Fe = [], Le = 0, je = 0; Le < Me.length; je = ++Le % 4)
                    je != 0 && Fe.push(($e.indexOf(Me.charAt(Le - 1)) & Math.pow(2, -2 * je + 8) - 1) << je * 2 | $e.indexOf(Me.charAt(Le)) >>> 6 - je * 2);
                return Fe
            }
        };
        pe.exports = Pe
    }
    )()
}), charenc = {
    utf8: {
        stringToBytes: function(pe) {
            return charenc.bin.stringToBytes(unescape(encodeURIComponent(pe)))
        },
        bytesToString: function(pe) {
            return decodeURIComponent(escape(charenc.bin.bytesToString(pe)))
        }
    },
    bin: {
        stringToBytes: function(pe) {
            for (var $e = [], Pe = 0; Pe < pe.length; Pe++)
                $e.push(pe.charCodeAt(Pe) & 255);
            return $e
        },
        bytesToString: function(pe) {
            for (var $e = [], Pe = 0; Pe < pe.length; Pe++)
                $e.push(String.fromCharCode(pe[Pe]));
            return $e.join("")
        }
    }
}
    , charenc_1 = charenc;

var isBuffer_1 = function(pe) {
    return pe != null && (isBuffer$2(pe) || isSlowBuffer(pe) || !!pe._isBuffer)
};
function isBuffer$2(pe) {
    return !!pe.constructor && typeof pe.constructor.isBuffer == "function" && pe.constructor.isBuffer(pe)
}
function isSlowBuffer(pe) {
    return typeof pe.readFloatLE == "function" && typeof pe.slice == "function" && isBuffer$2(pe.slice(0, 0))
}

var md5 = createCommonjsModule(function(pe) {
    (function() {
        var $e = crypt
          , Pe = charenc_1.utf8
          , Me = isBuffer_1
          , Fe = charenc_1.bin
          , Le = function(je, Be) {
            je.constructor == String ? Be && Be.encoding === "binary" ? je = Fe.stringToBytes(je) : je = Pe.stringToBytes(je) : Me(je) ? je = Array.prototype.slice.call(je, 0) : !Array.isArray(je) && je.constructor !== Uint8Array && (je = je.toString());
            for (var Ve = $e.bytesToWords(je), He = je.length * 8, ze = 1732584193, Ge = -271733879, We = -1732584194, Ye = 271733878, Qe = 0; Qe < Ve.length; Qe++)
                Ve[Qe] = (Ve[Qe] << 8 | Ve[Qe] >>> 24) & 16711935 | (Ve[Qe] << 24 | Ve[Qe] >>> 8) & 4278255360;
            Ve[He >>> 5] |= 128 << He % 32,
            Ve[(He + 64 >>> 9 << 4) + 14] = He;
            for (var it = Le._ff, at = Le._gg, Xe = Le._hh, Ke = Le._ii, Qe = 0; Qe < Ve.length; Qe += 16) {
                var qe = ze
                  , Ze = Ge
                  , Je = We
                  , st = Ye;
                ze = it(ze, Ge, We, Ye, Ve[Qe + 0], 7, -680876936),
                Ye = it(Ye, ze, Ge, We, Ve[Qe + 1], 12, -389564586),
                We = it(We, Ye, ze, Ge, Ve[Qe + 2], 17, 606105819),
                Ge = it(Ge, We, Ye, ze, Ve[Qe + 3], 22, -1044525330),
                ze = it(ze, Ge, We, Ye, Ve[Qe + 4], 7, -176418897),
                Ye = it(Ye, ze, Ge, We, Ve[Qe + 5], 12, 1200080426),
                We = it(We, Ye, ze, Ge, Ve[Qe + 6], 17, -1473231341),
                Ge = it(Ge, We, Ye, ze, Ve[Qe + 7], 22, -45705983),
                ze = it(ze, Ge, We, Ye, Ve[Qe + 8], 7, 1770035416),
                Ye = it(Ye, ze, Ge, We, Ve[Qe + 9], 12, -1958414417),
                We = it(We, Ye, ze, Ge, Ve[Qe + 10], 17, -42063),
                Ge = it(Ge, We, Ye, ze, Ve[Qe + 11], 22, -1990404162),
                ze = it(ze, Ge, We, Ye, Ve[Qe + 12], 7, 1804603682),
                Ye = it(Ye, ze, Ge, We, Ve[Qe + 13], 12, -40341101),
                We = it(We, Ye, ze, Ge, Ve[Qe + 14], 17, -1502002290),
                Ge = it(Ge, We, Ye, ze, Ve[Qe + 15], 22, 1236535329),
                ze = at(ze, Ge, We, Ye, Ve[Qe + 1], 5, -165796510),
                Ye = at(Ye, ze, Ge, We, Ve[Qe + 6], 9, -1069501632),
                We = at(We, Ye, ze, Ge, Ve[Qe + 11], 14, 643717713),
                Ge = at(Ge, We, Ye, ze, Ve[Qe + 0], 20, -373897302),
                ze = at(ze, Ge, We, Ye, Ve[Qe + 5], 5, -701558691),
                Ye = at(Ye, ze, Ge, We, Ve[Qe + 10], 9, 38016083),
                We = at(We, Ye, ze, Ge, Ve[Qe + 15], 14, -660478335),
                Ge = at(Ge, We, Ye, ze, Ve[Qe + 4], 20, -405537848),
                ze = at(ze, Ge, We, Ye, Ve[Qe + 9], 5, 568446438),
                Ye = at(Ye, ze, Ge, We, Ve[Qe + 14], 9, -1019803690),
                We = at(We, Ye, ze, Ge, Ve[Qe + 3], 14, -187363961),
                Ge = at(Ge, We, Ye, ze, Ve[Qe + 8], 20, 1163531501),
                ze = at(ze, Ge, We, Ye, Ve[Qe + 13], 5, -1444681467),
                Ye = at(Ye, ze, Ge, We, Ve[Qe + 2], 9, -51403784),
                We = at(We, Ye, ze, Ge, Ve[Qe + 7], 14, 1735328473),
                Ge = at(Ge, We, Ye, ze, Ve[Qe + 12], 20, -1926607734),
                ze = Xe(ze, Ge, We, Ye, Ve[Qe + 5], 4, -378558),
                Ye = Xe(Ye, ze, Ge, We, Ve[Qe + 8], 11, -2022574463),
                We = Xe(We, Ye, ze, Ge, Ve[Qe + 11], 16, 1839030562),
                Ge = Xe(Ge, We, Ye, ze, Ve[Qe + 14], 23, -35309556),
                ze = Xe(ze, Ge, We, Ye, Ve[Qe + 1], 4, -1530992060),
                Ye = Xe(Ye, ze, Ge, We, Ve[Qe + 4], 11, 1272893353),
                We = Xe(We, Ye, ze, Ge, Ve[Qe + 7], 16, -155497632),
                Ge = Xe(Ge, We, Ye, ze, Ve[Qe + 10], 23, -1094730640),
                ze = Xe(ze, Ge, We, Ye, Ve[Qe + 13], 4, 681279174),
                Ye = Xe(Ye, ze, Ge, We, Ve[Qe + 0], 11, -358537222),
                We = Xe(We, Ye, ze, Ge, Ve[Qe + 3], 16, -722521979),
                Ge = Xe(Ge, We, Ye, ze, Ve[Qe + 6], 23, 76029189),
                ze = Xe(ze, Ge, We, Ye, Ve[Qe + 9], 4, -640364487),
                Ye = Xe(Ye, ze, Ge, We, Ve[Qe + 12], 11, -421815835),
                We = Xe(We, Ye, ze, Ge, Ve[Qe + 15], 16, 530742520),
                Ge = Xe(Ge, We, Ye, ze, Ve[Qe + 2], 23, -995338651),
                ze = Ke(ze, Ge, We, Ye, Ve[Qe + 0], 6, -198630844),
                Ye = Ke(Ye, ze, Ge, We, Ve[Qe + 7], 10, 1126891415),
                We = Ke(We, Ye, ze, Ge, Ve[Qe + 14], 15, -1416354905),
                Ge = Ke(Ge, We, Ye, ze, Ve[Qe + 5], 21, -57434055),
                ze = Ke(ze, Ge, We, Ye, Ve[Qe + 12], 6, 1700485571),
                Ye = Ke(Ye, ze, Ge, We, Ve[Qe + 3], 10, -1894986606),
                We = Ke(We, Ye, ze, Ge, Ve[Qe + 10], 15, -1051523),
                Ge = Ke(Ge, We, Ye, ze, Ve[Qe + 1], 21, -2054922799),
                ze = Ke(ze, Ge, We, Ye, Ve[Qe + 8], 6, 1873313359),
                Ye = Ke(Ye, ze, Ge, We, Ve[Qe + 15], 10, -30611744),
                We = Ke(We, Ye, ze, Ge, Ve[Qe + 6], 15, -1560198380),
                Ge = Ke(Ge, We, Ye, ze, Ve[Qe + 13], 21, 1309151649),
                ze = Ke(ze, Ge, We, Ye, Ve[Qe + 4], 6, -145523070),
                Ye = Ke(Ye, ze, Ge, We, Ve[Qe + 11], 10, -1120210379),
                We = Ke(We, Ye, ze, Ge, Ve[Qe + 2], 15, 718787259),
                Ge = Ke(Ge, We, Ye, ze, Ve[Qe + 9], 21, -343485551),
                ze = ze + qe >>> 0,
                Ge = Ge + Ze >>> 0,
                We = We + Je >>> 0,
                Ye = Ye + st >>> 0
            }
            return $e.endian([ze, Ge, We, Ye])
        };
        Le._ff = function(je, Be, Ve, He, ze, Ge, We) {
            var Ye = je + (Be & Ve | ~Be & He) + (ze >>> 0) + We;
            return (Ye << Ge | Ye >>> 32 - Ge) + Be
        }
        ,
        Le._gg = function(je, Be, Ve, He, ze, Ge, We) {
            var Ye = je + (Be & He | Ve & ~He) + (ze >>> 0) + We;
            return (Ye << Ge | Ye >>> 32 - Ge) + Be
        }
        ,
        Le._hh = function(je, Be, Ve, He, ze, Ge, We) {
            var Ye = je + (Be ^ Ve ^ He) + (ze >>> 0) + We;
            return (Ye << Ge | Ye >>> 32 - Ge) + Be
        }
        ,
        Le._ii = function(je, Be, Ve, He, ze, Ge, We) {
            var Ye = je + (Ve ^ (Be | ~He)) + (ze >>> 0) + We;
            return (Ye << Ge | Ye >>> 32 - Ge) + Be
        }
        ,
        Le._blocksize = 16,
        Le._digestsize = 16,
        pe.exports = function(je, Be) {
            if (je == null)
                throw new Error("Illegal argument " + je);
            var Ve = $e.wordsToBytes(Le(je, Be));
            return Be && Be.asBytes ? Ve : Be && Be.asString ? Fe.bytesToString(Ve) : $e.bytesToHex(Ve)
        }
    }
    )()
});

function getKeyFromURL(pe) {
    return pe.substring(pe.lastIndexOf("/") + 1, pe.length).split(".")[0]
}

function getWbiKey(pe) {
    if (pe.useAssignKey)
        return {
            imgKey: pe.wbiImgKey,
            subKey: pe.wbiSubKey
        };
    var $e = localStorage.getItem("wbi_img_url")
      , Pe = localStorage.getItem("wbi_sub_url")
      , Me = $e ? getKeyFromURL($e) : pe.wbiImgKey
      , Fe = Pe ? getKeyFromURL(Pe) : pe.wbiSubKey;
    return {
        imgKey: Me,
        subKey: Fe
    }
}

function getMixinKey(pe) {
    var $e = [46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49, 33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13, 37, 48, 7, 16, 24, 55, 40, 61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11, 36, 20, 34, 44, 52]
      , Pe = [];
    return $e.forEach(function(Me) {
        pe.charAt(Me) && Pe.push(pe.charAt(Me))
    }),
    Pe.join("").slice(0, 32)
}

function encWbi(pe, $e) {
    $e || ($e = {});
    var Pe = getWbiKey($e)
      , Me = Pe.imgKey
      , Fe = Pe.subKey;
    // console.log(pe, $e, Pe, Me, Fe, '\n')
    if (Me && Fe) {
        for (var Le = getMixinKey(Me + Fe), je = Math.round(Date.now() / 1e3), Be = Object.assign({}, pe, {
            wts: je
        }), Ve = Object.keys(Be).sort(), He = [], ze = /[!'\(\)*]/g, Ge = 0; Ge < Ve.length; Ge++) {
            var We = Ve[Ge]
              , Ye = Be[We];
            Ye && typeof Ye == "string" && (Ye = Ye.replace(ze, "")),
            Ye != null && He.push("".concat(encodeURIComponent(We), "=").concat(encodeURIComponent(Ye)))
        }
        var Qe = He.join("&")
          , it = md5(Qe + Le);
        return {
            w_rid: it,
            wts: je.toString()
        }
    }
    return null
}

function js_encrypt(arg1) {
    return encWbi(arg1, $e)
}

var arg1 = {
    web_location: 1430650,
    y_num: 4,
    fresh_type: 4,
    feed_version: 'V8',
    fresh_idx_1h: 1,
    fetch_row: 4,
    fresh_idx: 1,
    brush: 1,
    homepage_ver: 1,
    ps: 12,
    last_y_num: 5,
    screen: 1920-413,
    outside_trigger: '',
    last_showlist: 'av_870647281,av_785722438,av_785662727,av_785734997,av_743279816,av_615584142,ad_n_5614,av_700702202,av_743070652,av_785754635',
    uniq_id: 243224006321
}


console.log(js_encrypt(arg1))