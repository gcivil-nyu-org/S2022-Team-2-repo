import { Record } from "./.fable/fable-library.3.1.7/Types.js";
import { lambda_type, unit_type, obj_type, float64_type, tuple_type, enum_type, array_type, option_type, bool_type, class_type, record_type, int32_type, string_type } from "./.fable/fable-library.3.1.7/Reflection.js";
import { succeed, andThen, tuple2, option, array, bool, int64, int, string, object } from "./.fable/Thoth.Json.5.1.0/Decode.fs.js";
import { uncurry } from "./.fable/fable-library.3.1.7/Util.js";
import DateOffset from "./.fable/fable-library.3.1.7/DateOffset.js";
import { fromBits, compare, toNumber } from "./.fable/fable-library.3.1.7/Long.js";
import { singleton, append } from "./.fable/fable-library.3.1.7/List.js";
import { object as object_1, toString, Enum_int } from "./.fable/Thoth.Json.5.1.0/Encode.fs.js";

export class MessageModelFile extends Record {
    constructor(id, url, name, size) {
        super();
        this.id = id;
        this.url = url;
        this.name = name;
        this.size = (size | 0);
    }
}

export function MessageModelFile$reflection() {
    return record_type("App.AppTypes.MessageModelFile", [], MessageModelFile, () => [["id", string_type], ["url", string_type], ["name", string_type], ["size", int32_type]]);
}

export function MessageModelFile_get_Decoder() {
    return (path_3) => ((v) => object((get$) => (new MessageModelFile(get$.Required.Field("id", (path, value) => string(path, value)), get$.Required.Field("url", (path_1, value_1) => string(path_1, value_1)), get$.Required.Field("name", (path_2, value_2) => string(path_2, value_2)), get$.Required.Field("size", uncurry(2, int)))), path_3, v));
}

export class MessageModel extends Record {
    constructor(id, text, sent, edited, read, file, sender, recipient, sender_username, out) {
        super();
        this.id = (id | 0);
        this.text = text;
        this.sent = sent;
        this.edited = edited;
        this.read = read;
        this.file = file;
        this.sender = sender;
        this.recipient = recipient;
        this.sender_username = sender_username;
        this.out = out;
    }
}

export function MessageModel$reflection() {
    return record_type("App.AppTypes.MessageModel", [], MessageModel, () => [["id", int32_type], ["text", string_type], ["sent", class_type("System.DateTimeOffset")], ["edited", class_type("System.DateTimeOffset")], ["read", bool_type], ["file", option_type(MessageModelFile$reflection())], ["sender", string_type], ["recipient", string_type], ["sender_username", string_type], ["out", bool_type]]);
}

export function MessageModel_get_Decoder() {
    return (path_6) => ((v) => object((get$) => (new MessageModel(get$.Required.Field("id", uncurry(2, int)), get$.Required.Field("text", (path, value) => string(path, value)), DateOffset(toNumber(get$.Required.Field("sent", uncurry(2, int64))) * 1000, 0), DateOffset(toNumber(get$.Required.Field("edited", uncurry(2, int64))) * 1000, 0), get$.Required.Field("read", (path_1, value_1) => bool(path_1, value_1)), get$.Optional.Field("file", uncurry(2, MessageModelFile_get_Decoder())), get$.Required.Field("sender", (path_2, value_2) => string(path_2, value_2)), get$.Required.Field("recipient", (path_3, value_3) => string(path_3, value_3)), get$.Required.Field("sender_username", (path_4, value_4) => string(path_4, value_4)), get$.Required.Field("out", (path_5, value_5) => bool(path_5, value_5)))), path_6, v));
}

export class MessagesResponse extends Record {
    constructor(page, pages, data) {
        super();
        this.page = (page | 0);
        this.pages = (pages | 0);
        this.data = data;
    }
}

export function MessagesResponse$reflection() {
    return record_type("App.AppTypes.MessagesResponse", [], MessagesResponse, () => [["page", int32_type], ["pages", int32_type], ["data", array_type(MessageModel$reflection())]]);
}

export function MessagesResponse_get_Decoder() {
    return (path_1) => ((v) => object((get$) => {
        let decoder;
        return new MessagesResponse(get$.Required.Field("page", uncurry(2, int)), get$.Required.Field("pages", uncurry(2, int)), get$.Required.Field("data", uncurry(2, (decoder = MessageModel_get_Decoder(), (path) => ((value) => array(uncurry(2, decoder), path, value))))));
    }, path_1, v));
}

export class UserInfoResponse extends Record {
    constructor(pk, username) {
        super();
        this.pk = pk;
        this.username = username;
    }
}

export function UserInfoResponse$reflection() {
    return record_type("App.AppTypes.UserInfoResponse", [], UserInfoResponse, () => [["pk", string_type], ["username", string_type]]);
}

export function UserInfoResponse_get_Decoder() {
    return (path_2) => ((v) => object((get$) => (new UserInfoResponse(get$.Required.Field("pk", (path, value) => string(path, value)), get$.Required.Field("username", (path_1, value_1) => string(path_1, value_1)))), path_2, v));
}

export class DialogModel extends Record {
    constructor(id, created, modified, other_user_id, unread_count, username, last_message) {
        super();
        this.id = (id | 0);
        this.created = created;
        this.modified = modified;
        this.other_user_id = other_user_id;
        this.unread_count = (unread_count | 0);
        this.username = username;
        this.last_message = last_message;
    }
}

export function DialogModel$reflection() {
    return record_type("App.AppTypes.DialogModel", [], DialogModel, () => [["id", int32_type], ["created", class_type("System.DateTimeOffset")], ["modified", class_type("System.DateTimeOffset")], ["other_user_id", string_type], ["unread_count", int32_type], ["username", string_type], ["last_message", option_type(MessageModel$reflection())]]);
}

export function DialogModel_get_Decoder() {
    return (path_3) => ((v) => object((get$) => {
        let decoder;
        return new DialogModel(get$.Required.Field("id", uncurry(2, int)), DateOffset(toNumber(get$.Required.Field("created", uncurry(2, int64))) * 1000, 0), DateOffset(toNumber(get$.Required.Field("modified", uncurry(2, int64))) * 1000, 0), get$.Required.Field("other_user_id", (path, value) => string(path, value)), get$.Required.Field("unread_count", uncurry(2, int)), get$.Required.Field("username", (path_1, value_1) => string(path_1, value_1)), get$.Required.Field("last_message", uncurry(2, (decoder = MessageModel_get_Decoder(), (path_2) => ((value_2) => option(uncurry(2, decoder), path_2, value_2))))));
    }, path_3, v));
}

export class DialogsResponse extends Record {
    constructor(page, pages, data) {
        super();
        this.page = (page | 0);
        this.pages = (pages | 0);
        this.data = data;
    }
}

export function DialogsResponse$reflection() {
    return record_type("App.AppTypes.DialogsResponse", [], DialogsResponse, () => [["page", int32_type], ["pages", int32_type], ["data", array_type(DialogModel$reflection())]]);
}

export function DialogsResponse_get_Decoder() {
    return (path_1) => ((v) => object((get$) => {
        let decoder;
        return new DialogsResponse(get$.Required.Field("page", uncurry(2, int)), get$.Required.Field("pages", uncurry(2, int)), get$.Required.Field("data", uncurry(2, (decoder = DialogModel_get_Decoder(), (path) => ((value) => array(uncurry(2, decoder), path, value))))));
    }, path_1, v));
}

export class MessageTypeNewUnreadCount extends Record {
    constructor(sender, unread_count) {
        super();
        this.sender = sender;
        this.unread_count = (unread_count | 0);
    }
}

export function MessageTypeNewUnreadCount$reflection() {
    return record_type("App.AppTypes.MessageTypeNewUnreadCount", [], MessageTypeNewUnreadCount, () => [["sender", string_type], ["unread_count", int32_type]]);
}

export function MessageTypeNewUnreadCount_get_Decoder() {
    return (path_1) => ((v) => object((get$) => (new MessageTypeNewUnreadCount(get$.Required.Field("sender", (path, value) => string(path, value)), get$.Required.Field("unread_count", uncurry(2, int)))), path_1, v));
}

export class MessageTypeMessageRead extends Record {
    constructor(message_id, sender, receiver) {
        super();
        this.message_id = message_id;
        this.sender = sender;
        this.receiver = receiver;
    }
}

export function MessageTypeMessageRead$reflection() {
    return record_type("App.AppTypes.MessageTypeMessageRead", [], MessageTypeMessageRead, () => [["message_id", class_type("System.Int64")], ["sender", string_type], ["receiver", string_type]]);
}

export function MessageTypeMessageRead_get_Decoder() {
    return (path_2) => ((v) => object((get$) => (new MessageTypeMessageRead(get$.Required.Field("message_id", uncurry(2, int64)), get$.Required.Field("sender", (path, value) => string(path, value)), get$.Required.Field("receiver", (path_1, value_1) => string(path_1, value_1)))), path_2, v));
}

export class MessageTypeTextMessage extends Record {
    constructor(random_id, text, sender, receiver, sender_username) {
        super();
        this.random_id = random_id;
        this.text = text;
        this.sender = sender;
        this.receiver = receiver;
        this.sender_username = sender_username;
    }
}

export function MessageTypeTextMessage$reflection() {
    return record_type("App.AppTypes.MessageTypeTextMessage", [], MessageTypeTextMessage, () => [["random_id", class_type("System.Int64")], ["text", string_type], ["sender", string_type], ["receiver", string_type], ["sender_username", string_type]]);
}

export function MessageTypeTextMessage_get_Decoder() {
    return (path_4) => ((v) => object((get$) => (new MessageTypeTextMessage(get$.Required.Field("random_id", uncurry(2, int64)), get$.Required.Field("text", (path, value) => string(path, value)), get$.Required.Field("sender", (path_1, value_1) => string(path_1, value_1)), get$.Required.Field("receiver", (path_2, value_2) => string(path_2, value_2)), get$.Required.Field("sender_username", (path_3, value_3) => string(path_3, value_3)))), path_4, v));
}

export class MessageTypeFileMessage extends Record {
    constructor(db_id, file, sender, receiver, sender_username) {
        super();
        this.db_id = db_id;
        this.file = file;
        this.sender = sender;
        this.receiver = receiver;
        this.sender_username = sender_username;
    }
}

export function MessageTypeFileMessage$reflection() {
    return record_type("App.AppTypes.MessageTypeFileMessage", [], MessageTypeFileMessage, () => [["db_id", class_type("System.Int64")], ["file", MessageModelFile$reflection()], ["sender", string_type], ["receiver", string_type], ["sender_username", string_type]]);
}

export function MessageTypeFileMessage_get_Decoder() {
    return (path_3) => ((v) => object((get$) => (new MessageTypeFileMessage(get$.Required.Field("db_id", uncurry(2, int64)), get$.Required.Field("file", uncurry(2, MessageModelFile_get_Decoder())), get$.Required.Field("sender", (path, value) => string(path, value)), get$.Required.Field("receiver", (path_1, value_1) => string(path_1, value_1)), get$.Required.Field("sender_username", (path_2, value_2) => string(path_2, value_2)))), path_3, v));
}

export class MessageTypeMessageIdCreated extends Record {
    constructor(random_id, db_id) {
        super();
        this.random_id = random_id;
        this.db_id = db_id;
    }
}

export function MessageTypeMessageIdCreated$reflection() {
    return record_type("App.AppTypes.MessageTypeMessageIdCreated", [], MessageTypeMessageIdCreated, () => [["random_id", class_type("System.Int64")], ["db_id", class_type("System.Int64")]]);
}

export function MessageTypeMessageIdCreated_get_Decoder() {
    return (path) => ((v) => object((get$) => (new MessageTypeMessageIdCreated(get$.Required.Field("random_id", uncurry(2, int64)), get$.Required.Field("db_id", uncurry(2, int64)))), path, v));
}

export class MessageTypeErrorOccurred extends Record {
    constructor(error) {
        super();
        this.error = error;
    }
}

export function MessageTypeErrorOccurred$reflection() {
    return record_type("App.AppTypes.MessageTypeErrorOccurred", [], MessageTypeErrorOccurred, () => [["error", tuple_type(enum_type("App.AppTypes.ErrorTypes", int32_type, [["MessageParsingError", 1], ["TextMessageInvalid", 2], ["InvalidMessageReadId", 3], ["InvalidUserPk", 4], ["InvalidRandomId", 5], ["FileMessageInvalid", 6], ["FileDoesNotExist", 7]]), string_type)]]);
}

export function MessageTypeErrorOccurred_get_Decoder() {
    return (path_2) => ((v) => object((get$) => (new MessageTypeErrorOccurred(get$.Required.Field("error", uncurry(2, tuple2((path, value_1) => andThen((value, arg10$0040, arg20$0040) => succeed(value, arg10$0040, arg20$0040), uncurry(2, int), path, value_1), (path_1, value_2) => string(path_1, value_2)))))), path_2, v));
}

export class GenericUserPKMessage extends Record {
    constructor(user_pk) {
        super();
        this.user_pk = user_pk;
    }
}

export function GenericUserPKMessage$reflection() {
    return record_type("App.AppTypes.GenericUserPKMessage", [], GenericUserPKMessage, () => [["user_pk", string_type]]);
}

export function GenericUserPKMessage_get_Decoder() {
    return (path_1) => ((v) => object((get$) => (new GenericUserPKMessage(get$.Required.Field("user_pk", (path, value) => string(path, value)))), path_1, v));
}

export function msgTypeEncoder(t, data) {
    const d = append(data, singleton(["msg_type", Enum_int(t)]));
    return toString(0, object_1(d));
}

export const MessageTypesDecoder = (path_1) => ((v) => object((get$) => get$.Required.Field("msg_type", (path, value_1) => andThen((value, arg10$0040, arg20$0040) => succeed(value, arg10$0040, arg20$0040), uncurry(2, int), path, value_1)), path_1, v));

export class MessageBoxDataStatus extends Record {
    constructor(click, loading, download) {
        super();
        this.click = click;
        this.loading = loading;
        this.download = download;
    }
}

export function MessageBoxDataStatus$reflection() {
    return record_type("App.AppTypes.MessageBoxDataStatus", [], MessageBoxDataStatus, () => [["click", bool_type], ["loading", float64_type], ["download", bool_type]]);
}

export class MessageBoxData extends Record {
    constructor(dialog_id, message_id, out, size, uri, status) {
        super();
        this.dialog_id = dialog_id;
        this.message_id = message_id;
        this.out = out;
        this.size = size;
        this.uri = uri;
        this.status = status;
    }
}

export function MessageBoxData$reflection() {
    return record_type("App.AppTypes.MessageBoxData", [], MessageBoxData, () => [["dialog_id", string_type], ["message_id", class_type("System.Int64")], ["out", bool_type], ["size", option_type(string_type)], ["uri", option_type(string_type)], ["status", option_type(MessageBoxDataStatus$reflection())]]);
}

export class MessageBox extends Record {
    constructor(position, type, text, title, status, avatar, date, data, onDownload) {
        super();
        this.position = position;
        this.type = type;
        this.text = text;
        this.title = title;
        this.status = status;
        this.avatar = avatar;
        this.date = date;
        this.data = data;
        this.onDownload = onDownload;
    }
}

export function MessageBox$reflection() {
    return record_type("App.AppTypes.MessageBox", [], MessageBox, () => [["position", string_type], ["type", string_type], ["text", string_type], ["title", string_type], ["status", string_type], ["avatar", string_type], ["date", class_type("System.DateTimeOffset")], ["data", MessageBoxData$reflection()], ["onDownload", option_type(lambda_type(obj_type, unit_type))]]);
}

export function MessageBox__HasDbId(this$) {
    return compare(this$.data.message_id, fromBits(0, 0, false)) > 0;
}

export class ChatItem extends Record {
    constructor(id, avatar, avatarFlexible, statusColor, statusColorType, alt, title, date, subtitle, unread) {
        super();
        this.id = id;
        this.avatar = avatar;
        this.avatarFlexible = avatarFlexible;
        this.statusColor = statusColor;
        this.statusColorType = statusColorType;
        this.alt = alt;
        this.title = title;
        this.date = date;
        this.subtitle = subtitle;
        this.unread = (unread | 0);
    }
}

export function ChatItem$reflection() {
    return record_type("App.AppTypes.ChatItem", [], ChatItem, () => [["id", string_type], ["avatar", string_type], ["avatarFlexible", bool_type], ["statusColor", string_type], ["statusColorType", option_type(string_type)], ["alt", string_type], ["title", string_type], ["date", class_type("System.DateTimeOffset")], ["subtitle", string_type], ["unread", int32_type]]);
}

export class State extends Record {
    constructor(socketConnectionState, messageList, dialogList, selectedDialog, socket) {
        super();
        this.socketConnectionState = (socketConnectionState | 0);
        this.messageList = messageList;
        this.dialogList = dialogList;
        this.selectedDialog = selectedDialog;
        this.socket = socket;
    }
}

export function State$reflection() {
    return record_type("App.AppTypes.State", [], State, () => [["socketConnectionState", int32_type], ["messageList", array_type(MessageBox$reflection())], ["dialogList", array_type(ChatItem$reflection())], ["selectedDialog", ChatItem$reflection()], ["socket", class_type("Browser.Types.WebSocket")]]);
}

