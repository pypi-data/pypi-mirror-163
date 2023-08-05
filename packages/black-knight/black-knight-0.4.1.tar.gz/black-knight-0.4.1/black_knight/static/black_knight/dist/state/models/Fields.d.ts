import type { PK, VWT_ALL, V_Bool, V_Date, V_DateTime, V_Decimal, V_File, V_ForeignKey, V_Image, V_ManyToMany, V_Time } from 'state';
interface BaseField<Value, Init = '' | Value, Choice = Value> {
    name: string;
    label: string;
    required: boolean;
    help_text: string;
    initial: Init;
    value?: Value;
    choices?: [Choice, string][];
}
interface CharField extends BaseField<string> {
    type: 'char';
    max_length?: number;
}
interface UrlField extends CharField {
    validation: 'url';
}
interface SlugField extends CharField {
    validation: 'slug';
    allow_unicode: boolean;
}
interface EmailField extends CharField {
    validation: 'email';
}
interface DurationField extends CharField {
    validation: 'duration';
}
interface UUIDField extends CharField {
    validation: 'uuid';
}
interface GenericIPAddressField extends CharField {
    validation: 'ip_address';
    protocol: 'both' | 'ipv4' | 'ipv6';
}
declare type CharBasedFields = CharField | UrlField | SlugField | EmailField | DurationField | UUIDField | GenericIPAddressField;
interface TextField extends BaseField<string> {
    type: 'text';
}
interface JsonField extends BaseField<string> {
    type: 'json';
}
interface BooleanField extends BaseField<V_Bool, V_Bool> {
    type: 'boolean';
}
interface IntegerField extends BaseField<number> {
    type: 'integer';
    min: number;
    max: number;
}
interface DecimalField extends BaseField<V_Decimal> {
    type: 'decimal';
    max_digits: number;
    decimal_places: number;
}
interface FloatField extends BaseField<number> {
    type: 'float';
}
interface ImageField extends BaseField<V_Image, string, string> {
    type: 'image';
}
interface FileField extends BaseField<V_File, string, string> {
    type: 'file';
}
interface FilePathField extends Omit<BaseField<string>, 'choices'> {
    type: 'file_path';
    choices: [string, string][];
}
interface DateField extends BaseField<V_Date, string> {
    type: 'date';
}
interface DateTimeField extends BaseField<V_DateTime, string> {
    type: 'datetime';
}
interface TimeField extends BaseField<V_Time, string> {
    type: 'time';
}
interface ForeignKeyField extends Omit<BaseField<V_ForeignKey, PK>, 'choices'> {
    type: 'foreign_key';
    choices: V_ForeignKey[];
}
interface ManyToManyField extends Omit<BaseField<V_ManyToMany, PK[]>, 'choices'> {
    type: 'many_to_many';
    choices: V_ManyToMany;
}
interface UnknownField {
    name: string;
    label: string;
    type: 'unknown';
}
interface ReadOnlyField {
    name: string;
    label: string;
    type: 'readonly';
    value?: VWT_ALL;
}
declare type Field = CharBasedFields | TextField | JsonField | BooleanField | IntegerField | DecimalField | FloatField | ImageField | FileField | FilePathField | DateField | DateTimeField | TimeField | ForeignKeyField | ManyToManyField | UnknownField | ReadOnlyField;
export { Field as FieldModel, CharBasedFields as CharBasedFieldsModel };
export { TextField as TextFieldModel, JsonField as JsonFieldModel, BooleanField as BooleanFieldModel, IntegerField as IntegerFieldModel, DecimalField as DecimalFieldModel, FloatField as FloatFieldModel, ImageField as ImageFieldModel, FileField as FileFieldModel, FilePathField as FilePathFieldModel, DateField as DateFieldModel, DateTimeField as DateTimeFieldModel, TimeField as TimeFieldModel, ForeignKeyField as ForeignKeyFieldModel, ManyToManyField as ManyToManyFieldModel, UnknownField as UnknownFieldModel, ReadOnlyField as ReadOnlyFieldModel, };
//# sourceMappingURL=Fields.d.ts.map