import { PK } from 'state';
interface TArgs {
    type: 'add' | 'remove';
    id: PK | 'all' | 'page';
}
declare const BraceSelectAtom: import("jotai").WritableAtom<PK[] | "all", TArgs, void>;
export { BraceSelectAtom };
//# sourceMappingURL=select.d.ts.map