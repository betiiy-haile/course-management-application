import { createClient } from '@supabase/supabase-js'

const SUPABASE_URL="https://pbtvxilblnitbgowcbjm.supabase.co";
const SUPABASE_ANON_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBidHZ4aWxibG5pdGJnb3djYmptIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDkzMjk0NjQsImV4cCI6MjAyNDkwNTQ2NH0.qA3eIO0T8Hkv8xwI7lVyQC7ERneTnnO13wGBTq06GM4";

export const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY)
