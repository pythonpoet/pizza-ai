import {gun} from "./mygun"
//import GUN from 'gun/gun'
import 'gun/sea';
import 'gun/axe';

//'http://100.101.54.114:8023/gun'
// Database
//import GUN from "https://cdn.skypack.dev/gun";
const db = gun

// Gun User
export const user = db.user().recall({sessionStorage: true});

import { writable } from 'svelte/store';

// Current User's username
export const username = writable('');

user.get('alias').on(v => username.set(v))
