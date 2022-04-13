import { defaultArg, value as value_1 } from "./.fable/fable-library.3.1.7/Option.js";
import { randomNext, int32ToString } from "./.fable/fable-library.3.1.7/Util.js";
import * as identicon from "identicon.js";
import { fromInteger } from "./.fable/fable-library.3.1.7/Long.js";
import { op_UnaryNegation_Int32 } from "./.fable/fable-library.3.1.7/Int32.js";
import { printf, toText } from "./.fable/fable-library.3.1.7/String.js";

export function hashFnv32a(str, asString, seed) {
    let hval = ((seed == null) ? -2128831035 : value_1(seed)) | 0;
    for (let i = 0; i <= str.length; i++) {
        hval ^= str.charCodeAt(i);
        hval = (((((hval + (hval << 1)) + (hval << 4)) + (hval << 7)) + (hval << 8)) + (hval << 24));
    }
    if (asString) {
        return ('0000000' + (hval >>> 0).toString(16)).substr(-8);
    }
    else {
        let copyOfStruct = (hval >> 0) | 0;
        return int32ToString(copyOfStruct);
    }
}

export function hash64(str) {
    let h1 = hashFnv32a(str, true, void 0);
    return h1 + hashFnv32a(h1 + str, true, void 0);
}

export const Identicon = identicon;

export function getPhotoString(inputString, size) {
    const size_1 = defaultArg(size, 20) | 0;
    const h = hash64(inputString);
    const i = new Identicon(h, {
        margin: 0,
        size: size_1,
    });
    return "data:image/png;base64," + i;
}

export function generateRandomId() {
    const r = {};
    return fromInteger(op_UnaryNegation_Int32(randomNext(0, 2147483647)), false, 2);
}

export function humanFileSize(size) {
    const i = Math.floor(Math.log(size) / Math.log(1024));
    const r = size / Math.pow(1024, i);
    const suffix = ["B", "kB", "MB", "GB", "TB"][~(~i)];
    return toText(printf("%.2f %s"))(r)(suffix);
}

