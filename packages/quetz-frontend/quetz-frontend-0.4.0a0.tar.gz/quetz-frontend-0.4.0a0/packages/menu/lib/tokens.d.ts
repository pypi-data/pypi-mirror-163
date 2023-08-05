import { IRankedMenu } from '@jupyterlab/ui-components';
import { Token } from '@lumino/coreutils';
import { ISignal } from '@lumino/signaling';
export declare type Profile = {
    name: string;
    avatar_url: string;
    user: {
        id: string;
        username: string;
    };
};
/**
 * The main menu token.
 */
export declare const IMenu: Token<IMenu>;
/**
 * The login menu interface.
 */
export interface IMenu extends Omit<IRankedMenu, 'menu'> {
    /**
     * Logged user profile.
     */
    readonly profile: Profile | null;
    /**
     * User profile changed signal.
     */
    readonly profileChanged: ISignal<IMenu, Profile | null>;
}
