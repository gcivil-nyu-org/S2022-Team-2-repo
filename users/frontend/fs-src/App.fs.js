import { DialogsResponse_get_Decoder, MessageBox__HasDbId, MessagesResponse_get_Decoder, UserInfoResponse_get_Decoder, MessageModelFile_get_Decoder, msgTypeEncoder, MessageTypesDecoder, MessageTypeNewUnreadCount_get_Decoder, MessageTypeMessageIdCreated_get_Decoder, MessageTypeErrorOccurred_get_Decoder, MessageTypeMessageRead_get_Decoder, MessageTypeFileMessage_get_Decoder, MessageTypeTextMessage_get_Decoder, GenericUserPKMessage_get_Decoder, MessageBox$reflection, ChatItem, MessageBox, MessageBoxData, MessageBoxDataStatus } from "./Types.fs.js";
import { PromiseBuilder__Delay_62FBFDE1, PromiseBuilder__Run_212F1D4B, mapResult } from "./.fable/Fable.Promise.2.0.0/Promise.fs.js";
import { map, defaultArg, some } from "./.fable/fable-library.3.1.7/Option.js";
import { promise } from "./.fable/Fable.Promise.2.0.0/PromiseImpl.fs.js";
import { Types_RequestProperties, tryFetch } from "./.fable/Fable.Fetch.2.2.0/Fetch.fs.js";
import { ofArray, singleton, empty } from "./.fable/fable-library.3.1.7/List.js";
import { Result_Map, Result_Bind, FSharpResult$2 } from "./.fable/fable-library.3.1.7/Choice.js";
import { generateRandomId, humanFileSize, getPhotoString } from "./Utils.fs.js";
import { now, fromDate } from "./.fable/fable-library.3.1.7/DateOffset.js";
import { Record } from "./.fable/fable-library.3.1.7/Types.js";
import { record_type, int32_type, bool_type, string_type, class_type, lambda_type, unit_type } from "./.fable/fable-library.3.1.7/Reflection.js";
import { toText, printf, toConsole } from "./.fable/fable-library.3.1.7/String.js";
import { array as array_3, fromString } from "./.fable/Thoth.Json.5.1.0/Decode.fs.js";
import { stringHash, uncurry } from "./.fable/fable-library.3.1.7/Util.js";
import { Enum_int, tuple2 } from "./.fable/Thoth.Json.5.1.0/Encode.fs.js";
import { fromInteger, toInt } from "./.fable/fable-library.3.1.7/Long.js";
import { sortBy, contains, map as map_1 } from "./.fable/fable-library.3.1.7/Array.js";
import { compare } from "./.fable/fable-library.3.1.7/Date.js";

export const defaultDataStatus = new MessageBoxDataStatus(true, 0, false);

export function createOnDownload(uri, filename, e) {
    const pr = mapResult((x) => {
        const u = URL.createObjectURL(x);
        const a = document.createElement("a");
        a.href = u;
        a.setAttribute("download", filename);
        a.click();
        void window.setTimeout((_arg1_1) => {
            URL.revokeObjectURL(u);
        }, 200);
    }, PromiseBuilder__Run_212F1D4B(promise, PromiseBuilder__Delay_62FBFDE1(promise, () => {
        console.log(some("running onDownload for " + uri));
        console.log(some(e));
        return tryFetch(uri, empty()).then(((_arg1) => {
            const resp = _arg1;
            if (resp.tag === 1) {
                const e_1 = resp.fields[0];
                return Promise.resolve((new FSharpResult$2(1, e_1.message)));
            }
            else {
                const r = resp.fields[0];
                return r.blob().then(((_arg2) => {
                    const b = _arg2;
                    return Promise.resolve((new FSharpResult$2(0, b)));
                }));
            }
        }));
    })));
    pr.then();
}

export function getSubtitleTextFromMessageModel(msg) {
    return defaultArg(map((x) => {
        if (x.out) {
            return "You: " + x.text;
        }
        else {
            return x.text;
        }
    }, msg), "");
}

export function getSubtitleTextFromMessageBox(msg) {
    return defaultArg(map((x) => {
        if (x.data.out) {
            return "You: " + x.text;
        }
        else {
            return x.text;
        }
    }, msg), "");
}

export function createMessageBoxFromMessageTypeTextMessage(message) {
    const avatar = getPhotoString(message.sender, 150);
    return new MessageBox("left", "text", message.text, message.sender_username, "waiting", avatar, fromDate(new Date()), new MessageBoxData(message.sender, message.random_id, false, void 0, void 0, void 0), void 0);
}

export function createMessageBoxFromMessageTypeFileMessage(message) {
    const avatar = getPhotoString(message.sender, 150);
    return new MessageBox("left", "file", message.file.name, message.sender_username, "waiting", avatar, fromDate(new Date()), new MessageBoxData(message.sender, message.db_id, false, humanFileSize(message.file.size), message.file.url, defaultDataStatus), (e) => {
        createOnDownload(message.file.url, message.file.name, e);
    });
}

export function createMessageBoxFromOutgoingMessage(text, user_pk, self_pk, self_username, random_id, file_data) {
    const avatar = getPhotoString(self_pk, 150);
    const dataStatus = map((_arg1) => defaultDataStatus, file_data);
    const size = map((x) => humanFileSize(x.size), file_data);
    const uri = map((x_1) => x_1.url, file_data);
    const tpe = (file_data != null) ? "file" : "text";
    return new MessageBox("right", tpe, text, self_username, "waiting", avatar, fromDate(new Date()), new MessageBoxData(user_pk, random_id, true, size, uri, dataStatus), map((x_2) => ((e) => {
        createOnDownload(x_2.url, x_2.name, e);
    }), file_data));
}

export function createNewDialogModelFromIncomingMessageBox(m) {
    return new ChatItem(m.data.dialog_id, getPhotoString(m.data.dialog_id, void 0), true, "lightgreen", void 0, m.title, m.title, m.date, m.text, 1);
}

export class WSHandlingCallbacks extends Record {
    constructor(addMessage, replaceMessageId, addPKToTyping, changePKOnlineStatus, setMessageIdAsRead, newUnreadCount) {
        super();
        this.addMessage = addMessage;
        this.replaceMessageId = replaceMessageId;
        this.addPKToTyping = addPKToTyping;
        this.changePKOnlineStatus = changePKOnlineStatus;
        this.setMessageIdAsRead = setMessageIdAsRead;
        this.newUnreadCount = newUnreadCount;
    }
}

export function WSHandlingCallbacks$reflection() {
    return record_type("App.WSHandlingCallbacks", [], WSHandlingCallbacks, () => [["addMessage", lambda_type(MessageBox$reflection(), unit_type)], ["replaceMessageId", lambda_type(class_type("System.Int64"), lambda_type(class_type("System.Int64"), unit_type))], ["addPKToTyping", lambda_type(string_type, unit_type)], ["changePKOnlineStatus", lambda_type(string_type, lambda_type(bool_type, unit_type))], ["setMessageIdAsRead", lambda_type(class_type("System.Int64"), unit_type)], ["newUnreadCount", lambda_type(string_type, lambda_type(int32_type, unit_type))]]);
}

export function handleIncomingWebsocketMessage(sock, message, callbacks) {
    const res = Result_Bind((o) => {
        switch (o) {
            case 1: {
                toConsole(printf("Received MessageTypes.WentOnline - %s"))(message);
                return Result_Map((d_2) => {
                    callbacks.changePKOnlineStatus(d_2.user_pk, true);
                }, fromString(uncurry(2, GenericUserPKMessage_get_Decoder()), message));
            }
            case 2: {
                toConsole(printf("Received MessageTypes.WentOffline - %s"))(message);
                return Result_Map((d_3) => {
                    callbacks.changePKOnlineStatus(d_3.user_pk, false);
                }, fromString(uncurry(2, GenericUserPKMessage_get_Decoder()), message));
            }
            case 3: {
                toConsole(printf("Received MessageTypes.TextMessage - %s"))(message);
                return Result_Map(callbacks.addMessage, Result_Map((message_1) => createMessageBoxFromMessageTypeTextMessage(message_1), fromString(uncurry(2, MessageTypeTextMessage_get_Decoder()), message)));
            }
            case 4: {
                toConsole(printf("Received MessageTypes.FileMessage - %s"))(message);
                return Result_Map(callbacks.addMessage, Result_Map((message_2) => createMessageBoxFromMessageTypeFileMessage(message_2), fromString(uncurry(2, MessageTypeFileMessage_get_Decoder()), message)));
            }
            case 5: {
                toConsole(printf("Received MessageTypes.IsTyping - %s"))(message);
                return Result_Map((d_1) => {
                    callbacks.addPKToTyping(d_1.user_pk);
                }, fromString(uncurry(2, GenericUserPKMessage_get_Decoder()), message));
            }
            case 6: {
                toConsole(printf("Received MessageTypes.MessageRead - %s"))(message);
                return Result_Map((d_4) => {
                    callbacks.setMessageIdAsRead(d_4.message_id);
                }, fromString(uncurry(2, MessageTypeMessageRead_get_Decoder()), message));
            }
            case 7: {
                toConsole(printf("Received MessageTypes.ErrorOccurred - %s"))(message);
                const decoded = fromString(uncurry(2, MessageTypeErrorOccurred_get_Decoder()), message);
                if (decoded.tag === 1) {
                    const e = decoded.fields[0];
                    return new FSharpResult$2(1, e);
                }
                else {
                    const err = decoded.fields[0];
                    const msg = toText(printf("Error: %A, message %s"))(err.error[0])(err.error[1]);
                    return new FSharpResult$2(1, msg);
                }
            }
            case 8: {
                toConsole(printf("Received MessageTypes.MessageIdCreated - %s"))(message);
                return Result_Map((d) => {
                    callbacks.replaceMessageId(d.random_id, d.db_id);
                }, fromString(uncurry(2, MessageTypeMessageIdCreated_get_Decoder()), message));
            }
            case 9: {
                toConsole(printf("Received MessageTypes.NewUnreadCount - %s"))(message);
                return Result_Map((d_5) => {
                    callbacks.newUnreadCount(d_5.sender, d_5.unread_count);
                }, fromString(uncurry(2, MessageTypeNewUnreadCount_get_Decoder()), message));
            }
            default: {
                const x = o | 0;
                toConsole(printf("Received unhandled MessageType %A"))(x);
                return new FSharpResult$2(0, void 0);
            }
        }
    }, fromString(uncurry(2, MessageTypesDecoder), message));
    if (res.tag === 1) {
        const e_1 = res.fields[0];
        toConsole(printf("Error while processing message %s - error: %s"))(message)(e_1);
        const data = singleton(["error", tuple2((value) => Enum_int(value), (value_1) => value_1, 1, toText(printf("msg_type decoding error - %s"))(e_1))]);
        sock.send(msgTypeEncoder(7, data));
        return toText(printf("Error occured - %s"))(e_1);
    }
    else {
        return void 0;
    }
}

export function sendOutgoingTextMessage(sock, text, user_pk, self_info) {
    toConsole(printf("Sending text message: \u0027%A\u0027, user_pk:\u0027%A\u0027"))(text)(user_pk);
    const randomId = generateRandomId();
    const data = ofArray([["text", text], ["user_pk", user_pk], ["random_id", ~(~toInt(randomId))]]);
    sock.send(msgTypeEncoder(3, data));
    return map((x) => createMessageBoxFromOutgoingMessage(text, user_pk, x.pk, x.username, randomId, void 0), self_info);
}

export function sendOutgoingFileMessage(sock, user_pk, file_data, self_info) {
    toConsole(printf("Sending file message: \u0027%s\u0027, user_pk:\u0027%s\u0027"))(file_data.id)(user_pk);
    const randomId = generateRandomId();
    const data = ofArray([["file_id", file_data.id], ["user_pk", user_pk], ["random_id", ~(~toInt(randomId))]]);
    sock.send(msgTypeEncoder(4, data));
    return map((x) => createMessageBoxFromOutgoingMessage(file_data.name, user_pk, x.pk, x.username, randomId, file_data), self_info);
}

export function sendIsTypingMessage(sock) {
    sock.send(msgTypeEncoder(5, empty()));
}

export function sendMessageReadMessage(sock, user_pk, message_id) {
    toConsole(printf("Sending \u0027read\u0027 message for message_id \u0027%i\u0027, user_pk:\u0027%A\u0027"))(message_id)(user_pk);
    const data = ofArray([["user_pk", user_pk], ["message_id", ~(~toInt(message_id))]]);
    sock.send(msgTypeEncoder(6, data));
}

export const backendUrl = window.location.host;

export const messagesEndpoint = toText(printf("/messages/"));

export const dialogsEndpoint = toText(printf("/dialogs/"));

export const selfEndpoint = toText(printf("/user/self"));

export const usersEndpoint = toText(printf("/user/friends"));

export const uploadEndpoint = toText(printf("/upload/"));

export const imageEndPoint = toText(printf("%s/user/image"))(backendUrl);

export function uploadFile(f, csrfToken) {
    return PromiseBuilder__Run_212F1D4B(promise, PromiseBuilder__Delay_62FBFDE1(promise, () => {
        const data = new FormData();
        data.append("file", f[0]);
        const headers_2 = new Types_RequestProperties(1, {
            ["X-CSRFToken"]: csrfToken,
        });
        const props = ofArray([new Types_RequestProperties(0, "POST"), new Types_RequestProperties(2, data), headers_2]);
        return tryFetch(uploadEndpoint, props).then(((_arg1) => {
            const resp = _arg1;
            if (resp.tag === 1) {
                const e = resp.fields[0];
                return Promise.resolve((new FSharpResult$2(1, e.message)));
            }
            else {
                const r = resp.fields[0];
                return r.text().then(((_arg2) => {
                    const text = _arg2;
                    const decoded = fromString(uncurry(2, MessageModelFile_get_Decoder()), text);
                    return Promise.resolve(decoded);
                }));
            }
        }));
    }));
}

export function fetchSelfInfo() {
    return PromiseBuilder__Run_212F1D4B(promise, PromiseBuilder__Delay_62FBFDE1(promise, () => (tryFetch(selfEndpoint, empty()).then(((_arg1) => {
        const resp = _arg1;
        if (resp.tag === 1) {
            const e = resp.fields[0];
            return Promise.resolve((new FSharpResult$2(1, e.message)));
        }
        else {
            const r = resp.fields[0];
            return r.text().then(((_arg2) => {
                const text = _arg2;
                const decoded = fromString(uncurry(2, UserInfoResponse_get_Decoder()), text);
                return Promise.resolve(decoded);
            }));
        }
    })))));
}

export function fetchUsersList(existing) {
    const existingPks = map_1((x) => x.id, existing);
    return mapResult((x_1) => map_1((dialog_1) => (new ChatItem(dialog_1.pk, dialog_1.image, true, "", void 0, dialog_1.first_name, dialog_1.first_name, now(), "", 0)), x_1.filter((dialog) => (!contains(dialog.pk, existingPks, {
        Equals: (x_2, y) => (x_2 === y),
        GetHashCode: (x_2) => stringHash(x_2),
    })))), PromiseBuilder__Run_212F1D4B(promise, PromiseBuilder__Delay_62FBFDE1(promise, () => (tryFetch(usersEndpoint, empty()).then(((_arg1) => {
        const resp = _arg1;
        if (resp.tag === 1) {
            const e = resp.fields[0];
            return Promise.resolve((new FSharpResult$2(1, e.message)));
        }
        else {
            const r = resp.fields[0];
            return r.text().then(((_arg2) => {
                let decoder;
                const text = _arg2;
                const decoded = fromString(uncurry(2, (decoder = UserInfoResponse_get_Decoder(), (path) => ((value) => array_3(uncurry(2, decoder), path, value)))), text);
                return Promise.resolve(decoded);
            }));
        }
    }))))));
}

export function fetchMessages() {
    return mapResult((x) => sortBy((x_4) => x_4.date, map_1((message) => {
        const t = (message.file != null) ? "file" : "text";
        let status;
        const matchValue_1 = [message.out, message.read];
        status = (matchValue_1[1] ? "read" : (matchValue_1[0] ? "sent" : "received"));
        const avatar = getPhotoString(message.sender, 150);
        const dialog_id = message.out ? message.recipient : message.sender;
        const dataStatus = map((_arg1_1) => defaultDataStatus, message.file);
        const size = map((x_1) => humanFileSize(x_1.size), message.file);
        const uri = map((x_2) => x_2.url, message.file);
        let text_1;
        const matchValue_2 = message.file;
        if (matchValue_2 == null) {
            text_1 = message.text;
        }
        else {
            const f = matchValue_2;
            text_1 = f.name;
        }
        return new MessageBox(message.out ? "right" : "left", t, text_1, message.sender_username, status, avatar, message.sent, new MessageBoxData(dialog_id, fromInteger(message.id, false, 2), message.out, size, uri, dataStatus), map((x_3) => ((e_1) => {
            createOnDownload(x_3.url, x_3.name, e_1);
        }), message.file));
    }, x.data), {
        Compare: (x_5, y) => compare(x_5, y),
    }), PromiseBuilder__Run_212F1D4B(promise, PromiseBuilder__Delay_62FBFDE1(promise, () => (tryFetch(messagesEndpoint, empty()).then(((_arg1) => {
        const resp = _arg1;
        if (resp.tag === 1) {
            const e = resp.fields[0];
            return Promise.resolve((new FSharpResult$2(1, e.message)));
        }
        else {
            const r = resp.fields[0];
            return r.text().then(((_arg2) => {
                const text = _arg2;
                const decoded = fromString(uncurry(2, MessagesResponse_get_Decoder()), text);
                return Promise.resolve(decoded);
            }));
        }
    }))))));
}

export function filterMessagesForDialog(d, messages) {
    if (d == null) {
        return new Array(0);
    }
    else {
        const dialog = d;
        return messages.filter((m) => (m.data.dialog_id === dialog.id));
    }
}

export function markMessagesForDialogAsRead(sock, d, messages, msgReadCallback) {
    filterMessagesForDialog(d, messages).filter((y) => {
        if ((y.status !== "read") ? (y.data.out === false) : false) {
            return MessageBox__HasDbId(y);
        }
        else {
            return false;
        }
    }).forEach((x) => {
        msgReadCallback(x.data.message_id);
        sendMessageReadMessage(sock, d.id, x.data.message_id);
    });
}

export function fetchDialogs() {
    return mapResult((x) => map_1((dialog) => (new ChatItem(dialog.other_user_id, getPhotoString(dialog.other_user_id, void 0), true, "", void 0, dialog.username, dialog.username, defaultArg(map((x_1) => x_1.sent, dialog.last_message), dialog.created), getSubtitleTextFromMessageModel(dialog.last_message), dialog.unread_count)), x.data), PromiseBuilder__Run_212F1D4B(promise, PromiseBuilder__Delay_62FBFDE1(promise, () => (tryFetch(dialogsEndpoint, empty()).then(((_arg1) => {
        const resp = _arg1;
        if (resp.tag === 1) {
            const e = resp.fields[0];
            return Promise.resolve((new FSharpResult$2(1, e.message)));
        }
        else {
            const r = resp.fields[0];
            return r.text().then(((_arg2) => {
                const text = _arg2;
                const decoded = fromString(uncurry(2, DialogsResponse_get_Decoder()), text);
                return Promise.resolve(decoded);
            }));
        }
    }))))));
}

